import turtle

def draw_recursive_edge(length, depth):
    if depth == 0:
        turtle.forward(length)
        return
    
    segment = length/3

    draw_recursive_edge(segment, depth-1)

    turtle.right(60)
    draw_recursive_edge(segment, depth-1)

    turtle.left(120)
    draw_recursive_edge(segment, depth-1)

    turtle.right(60)
    draw_recursive_edge(segment, depth-1)


def draw_recursive_polygon(sides, length, depth):
    angle = 360/sides
    for _ in range(sides):
        draw_recursive_edge(length, depth)
        turtle.right(angle)


def read_input(prompt, minimum):
    while True:
        try:
            value = int(input(prompt))
            if value >= minimum:
                return value
            print(f"Please enter a number greater than or equal to {minimum}")
        except ValueError:
            print("Invalid input! Please enter a valid integer")


def main():
    sides = read_input("Enter the number of sides: ", 3)
    length = read_input("Enter the side length: ", 1)
    depth = read_input("Enter the recursion depth: ", 0)

    screen = turtle.Screen()
    screen.title("Recursive Geometric Pattern")

    turtle.speed(0)
    turtle.penup()
    turtle.goto(-length/2, length/2)
    turtle.pendown()

    draw_recursive_polygon(sides, length, depth)

    turtle.hideturtle()
    turtle.done()


if __name__ == "__main__":
    main()