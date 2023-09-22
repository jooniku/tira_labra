import numpy as np

class ConvolutionalLayer:

    def __init__(self, kernel_size, stride_length=1) -> None:
        self.kernel_size = kernel_size
        self.stride_length = stride_length

        self.__create_kernel()

    def __create_kernel(self):
        """Creates the kernel that holds the weights.
        The weights are initialized to small random numbers.
        """
        # create weight matrix using numbers from numpys samples of "standard normal" distribution
        self.weight_matrix = 0.01 * np.random.randn(self.kernel_size, self.kernel_size) * np.sqrt(2.0 / self.kernel_size)
        self.bias_vector = np.array([0.01]*3)


    def _add_padding(self, image: np.array):
        """Adds zero-padding for the image to make sure the
        convolutions work.

        Args:
            image (np.array): array representation of image

        Returns:
            _type_: padded image
        """
        required_padding = (self.kernel_size - self.stride_length) // 2

        return np.pad(image, pad_width=required_padding)
    

    def _add_2d_convolution(self, raw_image: np.array):
        """For the image, multiply the image data with the
        weight matrix. Returns the multiplied image.

        Args:
            image (np.array): image to convolute
        """
        image = self._add_padding(image=raw_image)

        # reshape makes a copy??

        j = 0
        while j < 1:
            image_shape = image[np.ix_([i for i in range(j + self.kernel_size)])]
            j += self.kernel_size 

        #print(image_shape)
        return image





