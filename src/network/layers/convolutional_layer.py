import numpy as np


class ConvolutionalLayer:

    def __init__(self, filter_size, stride_length, num_of_filters):
        self.filter_size = filter_size
        self.num_of_filters = num_of_filters
        self.stride_length = stride_length
        self._create_filters()

    def _create_filters(self):
        """Creates the filter that holds the weights.
        The weights are initialized to small random numbers.
        """
        self.filters = [np.random.randn(self.filter_size,
                                        self.filter_size)
                        * np.sqrt(2.0 / self.filter_size*2)
                        for i in range(self.num_of_filters)]

        self.bias_vector = [0.01 for i in range(self.num_of_filters)]

    def add_padding(self, image: np.array):
        """Adds zero-padding for the image to make sure the
        operations work. All images are padded to be the
        same shape as the original input.
        """
        return image
        needed_padding = int(np.ceil(((self.stride_length - 1)*28
                                  -self.stride_length+self.filter_size)/2))
        #needed_padding = 0
        #if image.shape[1] < 32:
        #    needed_padding = int(np.ceil((32 - len(image)) / 2))

        return np.pad(image, pad_width=needed_padding)

    def add_2d_convolution(self, images):
        """This function is called for convolution. It
        calls the actual convolution function with 
        all filters in the convolutional layer and
        returns a 3D array with each filter activation.
        """
        images = np.array([self.add_padding(image) for image in images])
        self.received_inputs = images

        output_dim = int(
            (images.shape[1]-self.filter_size)/self.stride_length) + 1
        output_image = np.zeros((self.num_of_filters, output_dim, output_dim))
        self.conv_in_shape = images.shape

        for filter in range(len(self.filters)):
            filter_output = self._convolute2d(
                image=images[filter], filter=self.filters[filter], bias=self.bias_vector[filter])
            output_image[filter] += filter_output

        return output_image

    def _convolute2d(self, image, filter, bias):
        """This is the main convolution function. Using
        this class' filter, slide the filter across the
        image and add the bias vector. At each position, 
        calculate the sum of the dot products between filter
        and the local area.
        """
        output_image = []
        filter_y_pos = 0
        while filter_y_pos + self.filter_size <= image.shape[0]:
            filter_x_pos = 0
            output_image_sublist = []  # these act as the rows in the output image
            while filter_x_pos + self.filter_size <= image.shape[1]:
                local_area_sum = 0
                for row in range(len(filter)):
                    for column in range(len(filter)):
                        local_area_sum += image[filter_y_pos +
                                                row][filter_x_pos + column]*filter[row][column]
                output_image_sublist.append(local_area_sum + bias)
                filter_x_pos += self.stride_length
            output_image.append(output_image_sublist)
            filter_y_pos += self.stride_length

        output = np.array(output_image)
        return output

    def update_parameters(self, batch_size, learning_rate, beta1, beta2, iterations):
        """Updates the parameters with stored gradients
        from the backpropagation process.
        """

        for filter_i in range(len(self.filters)):
            # Update moment vectors
            self.filter_mean_grad[filter_i] = beta1*self.filter_mean_grad[filter_i] \
                + (1-beta1)*self.gradient_filters[filter_i]/batch_size
            self.filter_grad_variance[filter_i] = beta2*self.filter_grad_variance[filter_i] \
                + (1-beta2) * (self.gradient_filters[filter_i]/batch_size)**2
            # Take the bias-corrected variables
            filter_mhat = self.filter_mean_grad[filter_i] / \
                (1 - beta1**(iterations+1))
            filter_vhat = self.filter_grad_variance[filter_i] / (
                1 - beta2**(iterations+1))
            # Update variable
            self.filters[filter_i] -= learning_rate * \
                filter_mhat / (np.sqrt(filter_vhat)+1e-9)

            # Same for bias
            self.bias_mean_grad[filter_i] = beta1*self.bias_mean_grad[filter_i] \
                + (1-beta1)*self.bias_gradients[filter_i]/batch_size
            self.bias_grad_variance[filter_i] = beta2*self.bias_grad_variance[filter_i] \
                + (1-beta2) * (self.bias_gradients[filter_i]/batch_size)**2
            bias_mhat = self.bias_mean_grad[filter_i] / \
                (1 - beta1**(iterations+1))
            bias_vhat = self.bias_grad_variance[filter_i] / \
                (1 - beta2**(iterations+1))
            self.bias_vector[filter_i] -= learning_rate * \
                bias_mhat / (np.sqrt(bias_vhat)+1e-9)

    def initialize_gradients(self):
        """Initialize the gradients for
        the backpropagation process.
        The update follows the Adam optimization.
        """
        self.gradient_filters = np.zeros_like(self.filters)
        self.bias_gradients = np.zeros_like(self.bias_vector)

        self.filter_mean_grad = np.zeros_like(self.filters)
        self.filter_grad_variance = np.zeros_like(self.filters)

        self.bias_mean_grad = np.zeros_like(self.bias_vector)
        self.bias_grad_variance = np.zeros_like(self.bias_vector)

    def backpropagation(self, gradient_input, regularization_strength):
        """This function takes care of the backpropagation for the
        convolution layer. For each filter in the layer, it calls
        the _get_filter_gradient function to get the gradients for the filters
        and then updates the filters.
        """
        gradient_output = np.zeros(self.conv_in_shape)
        for filter_i in range(len(self.filters)):
            gradient_filter, d_out = self._get_filter_gradient(
                gradient_input=gradient_input[filter_i],
                filter=self.filters[filter_i],
                received_input=self.received_inputs[filter_i])
            # Add L2 regularization
            gradient_filter += regularization_strength * self.filters[filter_i]

            self.gradient_filters[filter_i] += gradient_filter

            self.bias_gradients[filter_i] += np.sum(gradient_input[filter_i])

            gradient_output[filter_i] = d_out

        return gradient_output

    def _get_filter_gradient(self, gradient_input, filter, received_input):
        """Gets the filter's and bias' gradients with respect to 
        the received input. Also computes the gradient from current
        filter to the next layer.
        """
        gradient_filter = np.zeros_like(filter)
        gradient_output = np.zeros(
            (self.conv_in_shape[1], self.conv_in_shape[2]))
        filter_height, filter_width = filter.shape

        current_y_pos = output_y_pos = 0
        while current_y_pos + self.filter_size <= self.conv_in_shape[1]:
            current_x_pos = output_x_pos = 0
            while current_x_pos + self.filter_size <= self.conv_in_shape[2]:

                # gets a local region of the filters size
                input_region = received_input[current_y_pos:current_y_pos +
                                              filter_height,
                                              current_x_pos:current_x_pos+filter_width]
                region_gradient = gradient_input[output_y_pos,
                                                 output_x_pos] * input_region

                gradient_filter += region_gradient

                gradient_output[current_y_pos:current_y_pos+filter_height,
                                current_x_pos:current_x_pos+filter_width] \
                    += gradient_input[output_y_pos, output_x_pos] * filter

                current_x_pos += self.stride_length
                output_x_pos += 1
            current_y_pos += self.stride_length
            output_y_pos += 1

        return gradient_filter, gradient_output

    def backpropagation1(self, gradient_input, regularization_strength):
        """This function takes care of the backpropagation for the
        convolution layer. For each filter in the layer, it calls
        the _get_filter_gradient function to get the gradients for the filters
        and then updates the filters.
        """
        gradient_output = np.zeros(self.conv_in_shape)
        for filter_i in range(len(self.filters)):
            current_y = output_y = 0
            while current_y + self.filter_size <= self.conv_in_shape[2]:
                current_x = output_x = 0
                while current_x + self.filter_size <= self.conv_in_shape[1]:

                    self.gradient_filters[filter_i] += gradient_input[filter_i, output_y, output_x]\
                        * self.received_inputs[filter_i, current_y:current_y+self.filter_size,
                                               current_x:current_x+self.filter_size]
                    gradient_output[filter_i, current_y:current_y+self.filter_size]\
                        * gradient_input[filter_i, output_y, output_x] * self.filters[filter_i]
                    current_x += self.stride_length
                    output_x += 1
                current_y += self.stride_length
                output_y += 1
            self.bias_gradients[filter_i] += np.sum(gradient_input[filter_i])

        return gradient_output
