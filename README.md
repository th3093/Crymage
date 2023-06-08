# Crymage
Encrypt and Decrypt Text Messages to .png files

The initial thought was to implement a small application to transfer e2e encrypted text messages.
This is based on a shared image in .png format.
Sender and receiver both has the same image as their private key.
Encryption and decryption is based on this key (image).

The encryption algorithm is simple, but thought and coded from scratch.
Only for image handling the python library pillow (PIL) is used. 

In this early version only RGB channels get modificated, so there is improvement when it comes to dark key images.
Therefor it is recommended to use bright ones like the examples.

____________________________________

For easy use, start gui.py for simple gui application.
console use is available via crymage.py (for further information look into documentation in code)

run requirements.txt for setup packages (only pillow) 
