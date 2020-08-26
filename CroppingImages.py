import pygame, sys

def newSurfaceSize(image, cropMethod, newWidth, newHeight):
    '''This function returns the size of a new surface on which
    the final image will be pasted.'''
    # current image size
    currentSize = image.get_rect().width, image.get_rect().height
    if cropMethod == 'pixels':
        # cropping out a specific number of pixels
        newSize = newWidth, newHeight
    elif cropMethod == 'proportion':
        # cropping out a specified proportion of the original image
        newSize = currentSize[0]*newWidth, currentSize[1]*newHeight
    # if another method name is entered
    else:
        print('Invalid method.' +
              'Method can only be either "pixels" or "proportion."')
    return newSize

def cropImage(image, cropMethod, newWidth, newHeight, position=(0,0),
              shiftLeft=0, shiftUp=0):
    '''This function crops an image laterally and/or vertically (neither
    diagonally nor free-form) and returns the new surface on which
    the final image will be pasted.
    position refers to the position of the cropped image with regard to
    the new surface on which the image will be pasted.
    The parameters shiftLeft and shiftUp refer to how much the right and
    the bottom sides of the image will be cropped out.
    The default is to crop out the left and/or top sides of the image.'''
    # current image size and new surface size
    currentSize = image.get_rect().width, image.get_rect().height
    newSize = newSurfaceSize(image, cropMethod, newWidth, newHeight)
    # number of top and/or left pixels to be cropped out
    if cropMethod == 'pixels':
        # cropping out a specific number of pixels
        cropped = (currentSize[0]-newSize[0]-shiftLeft,
                   currentSize[1]-newSize[1]-shiftUp)
    elif cropMethod == 'proportion':
        # cropping out a specified proportion of the original image
        cropped = (currentSize[0]-newSize[0]-currentSize[0]*shiftLeft,
                   currentSize[1]-newSize[1]-currentSize[1]*shiftUp)
    # if another method name is entered
    else:
        print('Invalid method.' +
              'Method can only be either "pixels" or "proportion."')
    # create a new surface on which cropped image will be pasted
    newSurface = pygame.Surface(newSize, pygame.SRCALPHA, 32)
    # paste cropped image onto the new surface
    newSurface.blit(image, position, cropped + newSize)
    return newSurface
