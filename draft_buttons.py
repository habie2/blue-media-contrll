from gpiozero import Button
button = Button(2)
while True:
    if button.is_pressed:
        print('You pushed me')
        


button.wait_for_press()
print('You pushed me')