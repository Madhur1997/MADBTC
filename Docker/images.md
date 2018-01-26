### Basic Terminology

An important distinction to be aware of when it comes to images is the difference between base and child images.

1. **Base images** are images that have no parent image, usually images with an OS like ubuntu, busybox or debian.

2. **Child images** are images that build on base images and add additional functionality.

Then there are official and user images, which can be both base and child images.

1. **Official images** are images that are officially maintained and supported by the folks at Docker. These are typically one word long. In the list of images above, the python, ubuntu, busybox and hello-world images are base images.

2. **User images** are images created and shared by users like you and me. They build on base images and add additional functionality. Typically, these are formatted as user/image-name.

All images are avaialable on **Docker hub**
and can be searched from terminal using
```bash
docker search
```
* What is a onbuild version ?

These images include multiple ONBUILD triggers, which should be all you need to bootstrap most applications. the onbuild version of the image includes helpers that automate the boring parts of getting an app running. Rather than doing these tasks manually (or scripting these tasks), these images do that work for you.

* Renaming a docker image ?

```bash
docker tag oldname newname
docker rmi oldname
```
