# Insta-Bot

At the time of writing this, instagram home-page
structure is as follows:

Each post which we see in the instagram feed, has
an actual-photo and like-button among other things.

We exploit this DOM (Document Object Model) structure
here to access the like-button and perform our
operation.

Note: Instagram loads the images in a bizzare manner.
First call to load the home-page (i.e. instagram feed)
will load only few (i.e. 4 or 5) images. As we scroll
down, it adds new images to the feed.
After a certain count (say 7 or 8 images), when the
next image will be laoded, it will be placed on the
top (i.e. first image content will be overwritten with
this new image content).
This process might be efficient for instagram, but it
makes our bot-programming a bit tedious.
