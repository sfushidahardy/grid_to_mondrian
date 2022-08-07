import random
from PIL import Image

#First, the code receives the grid data.
print('Before proceeding, check the README for formatting.')
print('Input your grid size.')
grid_size = int(input())
print('Next, input the grid data row by row.')

grid = list(range(grid_size))
for i in range(grid_size):
    grid[i] = [int(item) for item in input().split()]

#Next, the grid diagram data is checked for validity.

#Check that every row has exactly two 1s and the rest are 0s.
for i in range(grid_size):
    if grid[i].count(1) != 2 or grid[i].count(0) != grid_size-2:
        print('Your grid diagram isn\'t valid! Check your rows.')
        quit()

for i in range(grid_size):
    grid_column_i = [grid[j][i] for j in range(grid_size)]
    if grid_column_i.count(1) != 2 or grid_column_i.count(0) != grid_size-2:
        print('Your grid diagram isn\'t valid! Check your columns.')
        quit()

print('Success! Your grid diagram is valid.')

#This is just a function to help me debug, by printing lists of lists like tables :p
def matrix_printer(list_of_lists):
    for s in list_of_lists:
        print(*s)

#Next, we want to start determining rectangular regions.
#The first step is to enlarge the grid. We'll make it quite large, so that it encodes both faces and edges.
#Naively the grid diagram to Mondrian pipeline suffices to triple the grid size to encode faces. We'll actually sextuple the grid to also encode edges.

big_grid_size = 6*grid_size + 1
paint_grid = list(range(big_grid_size))
for j in range(big_grid_size):
    paint_grid[j] = [0]*big_grid_size

#For now the paint_grid is a giant matrix of 0s. In the remainder of the code, the 0s will be replaced with other numbers to indicate colour - eventually this matrix becomes the Mondrian!

mid_grid_size = 3*grid_size
knot_grid = list(range(mid_grid_size))
for i in range(mid_grid_size):
    knot_grid[i] = [0]*mid_grid_size
for j in range(grid_size):
    for i in range(grid_size):
        knot_grid[3*j+1][3*i+1] = grid[j][i]

knot_grid_aux = list(range(mid_grid_size))
for i in range(mid_grid_size):
    knot_grid_aux[i] = [0]*mid_grid_size
for j in range(grid_size):
    for i in range(grid_size):
        knot_grid_aux[3*j+1][3*i+1] = grid[j][i]
#This is an auxiliary grid in which we'll label every cell for which the knot lies over the cell.

#Next we'll keep a list of all of the coordinates of the knot which have yet to be painted.
#Similarly, we'll have a list of all of the coordinates of the "white space" which have yet to be painted.
#By updating these as we iterate the painting process, we'll randomly find rectangles to paint in an eventually-terminating process.

#Specifically, we're first starting by labelling all of the cells in the knot_grid with a 1 if the knot lies on the cell.
for j in range(mid_grid_size):
    try:
        left_1_pos = knot_grid[j].index(1)
    except ValueError:
        left_1_pos = 0
    try:
        right_1_pos = mid_grid_size - knot_grid[j][::-1].index(1) - 1
    except ValueError:
        right_1_pos = 0
    for i in range(left_1_pos+1, right_1_pos):
        knot_grid_aux[j][i] = 1

for i in range(mid_grid_size):
    grid_col_i = [knot_grid[n][i] for n in range(mid_grid_size)]
    try:
        top_1_pos = grid_col_i.index(1)
    except ValueError:
        top_1_pos = 0
    try:
        bottom_1_pos = mid_grid_size - grid_col_i[::-1].index(1) - 1
    except ValueError:
        bottom_1_pos = 0
    for j in range(top_1_pos+1, bottom_1_pos):
        knot_grid_aux[j][i] = 1

list_of_unpainted_knot_coords = []
list_of_unpainted_bg_coords = []
for j in range(mid_grid_size):
    for i in range(mid_grid_size):
        if knot_grid_aux[j][i] == 1:
            list_of_unpainted_knot_coords.append([j,i])
        else:
            list_of_unpainted_bg_coords.append([j,i])

#knot_grid contains an enlarged grid diagram. We'll use this to determine how to paint the matrix paint_grid.

#The first step in painting is to paint all of the crossings of the grid diagram. This guarantees that the Mondrian at the end actually really contains the original knot/link.

#This function checks if the cell (j,i) in a lattice occurs at a crossing.
def check_cell_for_crossing(j,i,lattice):
    dim = len(lattice)
    left_1_pos = lattice[j].index(1)
    right_1_pos = dim - lattice[j][::-1].index(1) - 1
    grid_column_i = [grid[n][i] for n in range(dim)]
    top_1_pos = grid_column_i.index(1)
    bottom_1_pos = dim - grid_column_i[::-1].index(1) - 1

    if left_1_pos < i and right_1_pos > i and top_1_pos < j and bottom_1_pos > j:
        return True
    else: return False

#This function paints crossings (i.e. assigns numbers).
def paint_crossing(j,i):
    colour = random.randint(3,5)
    colour_2 = colour + 1
    for n in range(5):
        paint_grid[6*j+1+n][6*i+3] = colour
        if n%2 == 0:
            list_of_unpainted_knot_coords.remove([3*j+n/2, 3*i+1])
    list_of_unpainted_knot_coords.remove([3*j+1,3*i])
    list_of_unpainted_knot_coords.remove([3*j+1,3*i+2])
    paint_grid[6*j+3][6*i+1] = colour_2
    paint_grid[6*j+3][6*i+5] = colour_2
    #we also want to add a black border around the newfound rectangle
    paint_grid[6*j+3][6*i] = 2
    paint_grid[6*j+2][6*i] = 2
    paint_grid[6*j+4][6*i] = 2
    paint_grid[6*j+2][6*i+1] = 2
    paint_grid[6*j+4][6*i+1] = 2

    paint_grid[6*j+3][6*i+6] = 2
    paint_grid[6*j+2][6*i+6] = 2
    paint_grid[6*j+4][6*i+6] = 2
    paint_grid[6*j+2][6*i+5] = 2
    paint_grid[6*j+4][6*i+5] = 2

    paint_grid[6*j][6*i+3] = 2
    paint_grid[6*j+6][6*i+3] = 2
    for n in range(7):
        paint_grid[6*j+n][6*i+2] = 2
        paint_grid[6*j+n][6*i+4] = 2

#We now check for cells in the grid diagram that lie on crossings. For those that do, we paint the three cells (one above and one below) the crossing a random colour from 3 to 5. The "edges" around these cells are painted 2.

#Note: 0 is unpainted, 1 is white, 2 is black, 3, 4, 5 are blue, red, yellow.

for i in range(grid_size):
    for j in range(grid_size):
        if grid[j][i] == 0:
            if check_cell_for_crossing(j,i,grid):
                paint_crossing(j,i)

#The next step is to paint the rest of the knot! This involves a few steps: first, choose a random unpainted cell lying on the knot. (This is in knot_grid) Next, we choose a random rectangle lying in the knot (but with bounded size). Finally this gets painted, updating the canvas and shrinking the sample space for the subsequent iteration.

#This function finds the largest potential rectangle in a knot containing a given cell
def find_big_rectangle_in_knot(coords):
    col_pos = coords[1]
    row_pos = coords[0]
    col_pos_left_extent = col_pos
    while knot_grid_aux[row_pos][col_pos_left_extent - 1] == 1:
        col_pos_left_extent = col_pos_left_extent - 1
    col_pos_right_extent = col_pos
    while knot_grid_aux[row_pos][col_pos_right_extent + 1] == 1:
        col_pos_right_extent = col_pos_right_extent + 1
    horizontal_extent = [col_pos_left_extent, col_pos_right_extent]
    row_pos_top_extent = row_pos
    while knot_grid_aux[row_pos_top_extent-1][col_pos] == 1:
        row_pos_top_extent = row_pos_top_extent - 1
    row_pos_bottom_extent = row_pos
    while knot_grid_aux[row_pos_bottom_extent+1][col_pos] == 1:
        row_pos_bottom_extent = row_pos_bottom_extent + 1
    vertical_extent = [row_pos_top_extent, row_pos_bottom_extent]
    if horizontal_extent[1] - horizontal_extent[0] >= vertical_extent[1] - vertical_extent[0]:
        rectangle_limits = [[row_pos, n] for n in range(horizontal_extent[0], horizontal_extent[1]+1)]
        direction = 'horizontal'
    else:
        rectangle_limits = [[n, col_pos] for n in range(vertical_extent[0], vertical_extent[1]+1)]
        direction = 'vertical'
    return [rectangle_limits, direction]

#This function lets me intersect two lists
def intersection(lst1, lst2):
    lst3 = [val for val in lst1 if val in lst2]
    return lst3

#This function takes the largest potential rectangle and replaces it with a bounded rectangle
def restrict_to_random_rectangle(coords, potential, drctn):
    minimum = random.randint(0,1)
    maximum = random.randint(0,1)
    if drctn == 'horizontal':
        temp_list = [[coords[0], i] for i in range(coords[1]-minimum, coords[1]+maximum+1)]
    else:
        temp_list = [[i, coords[1]] for i in range(coords[0]-minimum, coords[0]+maximum+1)]
    return intersection(temp_list, potential)

#This function ensures we don't repaint over already-painted cells
def restrict_to_unpainted_knot(potential):
    return intersection(list_of_unpainted_knot_coords, potential)

#This is the actual painting step, given coordinates for painting
def paint_rectangle(cells_to_paint, drctn):
    first_cell = cells_to_paint[0]
    last_cell = cells_to_paint[-1]
    colour = random.randint(3,5)
    chance_for_black = random.randint(0,7)
    if chance_for_black == 0:
        colour = 2
    if drctn == 'horizontal':
        for n in range(2*first_cell[1]+1, 2*last_cell[1]+2):
            paint_grid[2*first_cell[0]+1][n] = colour
            paint_grid[2*first_cell[0]][n] = 2
            paint_grid[2*first_cell[0]+2][n] = 2
        for m in range(3):
            paint_grid[2*first_cell[0]+m][2*first_cell[1]] = 2
            paint_grid[2*first_cell[0]+m][2*last_cell[1]+2] = 2
    else:
        for n in range(2*first_cell[0]+1,2*last_cell[0]+2):
            paint_grid[n][2*first_cell[1]+1] = colour
            paint_grid[n][2*first_cell[1]] = 2
            paint_grid[n][2*first_cell[1]+2] = 2
        for m in range(3):
            paint_grid[2*first_cell[0]][2*first_cell[1]+m] = 2
            paint_grid[2*last_cell[0]+2][2*first_cell[1]+m] = 2
    return

#This is a loop over all of the unpainted cells in the knot. Through this loop we choose an unpainted rectangle, paint it, and remove those cells from the list of unpainted coordinates.
while list_of_unpainted_knot_coords != []:
    cell = random.choice(list_of_unpainted_knot_coords)
    wide_range = find_big_rectangle_in_knot(cell)[0]
    direction = find_big_rectangle_in_knot(cell)[1]
    rand_range = restrict_to_random_rectangle(cell, wide_range, direction)
    actual_range = restrict_to_unpainted_knot(rand_range)
    paint_rectangle(actual_range, direction)
    for i in actual_range:
        list_of_unpainted_knot_coords.remove(i)

#Next, we'll follow a similar procedure to painting the knot, but instead to paint the exterior of the knot. We'll allow for bigger rectangles too, since they can have thickness now! 
#Specifically, our code will: first choose a random unpainted cell. Next, check a maximal rectangle within the paint grid obtained by shifting a unit at a time both horizontally and vertically. The largest rectangle of zeros is our potential rectangle space. Finally, paint this rectangle, and remove the painted cells from the list of unpainted cells.

def find_big_unpainted_rectangle(coords):
    C = coords
    No = max(0, coords[0]-1)
    So = min(mid_grid_size-1, coords[0]+1)
    We = max(0, coords[1]-1)
    Ea = min(mid_grid_size-1, coords[1]+1)
    NW = [No, We]
    N = [No, C[1]]
    NE = [No, Ea]
    W = [C[0], We]
    E = [C[0], Ea]
    SW = [So, We]
    S = [So, C[1]]
    SE = [So, Ea]

    mid_mid = [2*coords[0]+1, 2*coords[1]+1]
    top_value = max(1, 2*coords[0]-1)
    bottom_value = min(big_grid_size-2, 2*coords[0]+3)
    left_value = max(1, 2*coords[1]-1)
    right_value = min(big_grid_size-2, 2*coords[1]+3)
    top_left = [top_value, left_value]
    top_mid = [top_value, mid_mid[1]]
    top_right = [top_value, right_value]
    mid_left = [mid_mid[0], left_value]
    mid_right = [mid_mid[0], right_value]
    bot_left = [bottom_value, left_value]
    bot_mid = [bottom_value, mid_mid[1]]
    bot_right = [bottom_value, right_value]
    cell_coords = []
    if paint_grid[top_left[0]][top_left[1]] == 0 and paint_grid[top_right[0]][top_right[1]] == 0 and paint_grid[bot_left[0]][bot_left[1]] == 0 and paint_grid[bot_right[0]][bot_right[1]] == 0:
        cell_coords = [NW, N, NE, W, C, E, SW, S, SE]
    elif paint_grid[top_left[0]][top_left[1]] == 0 and paint_grid[top_right[0]][top_right[1]] == 0 and paint_grid[mid_left[0]][mid_left[1]] == 0 and paint_grid[mid_right[0]][mid_right[1]] == 0:
        cell_coords = [NW, N, NE, W, C, E]
    elif paint_grid[mid_left[0]][mid_left[1]] == 0 and paint_grid[mid_right[0]][mid_right[1]] == 0 and paint_grid[bot_left[0]][bot_left[1]] == 0 and paint_grid[bot_right[0]][bot_right[1]] == 0:
        cell_coords = [W, C, E, SW, S, SE]
    elif paint_grid[top_left[0]][top_left[1]] == 0 and paint_grid[top_mid[0]][top_mid[1]] == 0 and paint_grid[bot_left[0]][bot_left[1]] == 0 and paint_grid[bot_mid[0]][bot_mid[1]] == 0:
        cell_coords = [NW, N, W, C, SW, S]
    elif paint_grid[top_mid[0]][top_mid[1]] == 0 and paint_grid[top_right[0]][top_right[1]] == 0 and paint_grid[bot_mid[0]][bot_mid[1]] == 0 and paint_grid[bot_right[0]][bot_right[1]] == 0:
        cell_coords = [N, NE, C, E, S, SE]
    elif paint_grid[top_left[0]][top_left[1]] == 0 and paint_grid[top_mid[0]][top_mid[1]] == 0 and paint_grid[mid_left[0]][mid_left[1]] == 0:
        cell_coords = [NW, N, W, C]
    elif paint_grid[top_mid[0]][top_mid[1]] == 0 and paint_grid[top_right[0]][top_right[1]] == 0 and paint_grid[mid_right[0]][mid_right[1]] == 0:
        cell_coords = [N, NE, C, E]
    elif paint_grid[mid_left[0]][mid_left[1]] == 0 and paint_grid[bot_left[0]][bot_left[1]] == 0 and paint_grid[bot_mid[0]][bot_mid[1]] == 0:
        cell_coords = [W, C, SW, S]
    elif paint_grid[mid_right[0]][mid_right[1]] == 0 and paint_grid[bot_mid[0]][bot_mid[1]] == 0 and paint_grid[bot_right[0]][bot_right[1]] == 0:
        cell_coords = [C, E, S, SE]
    elif paint_grid[top_mid[0]][top_mid[1]] == 0 and paint_grid[bot_mid[0]][bot_mid[1]] == 0:
        cell_coords = [N, C, S]
    elif paint_grid[mid_left[0]][mid_left[1]] == 0 and paint_grid[mid_right[0]][mid_right[1]] == 0:
        cell_coords = [W, C, E]
    elif paint_grid[top_mid[0]][top_mid[1]] == 0:
        cell_coords = [N, C]
    elif paint_grid[mid_left[0]][mid_left[1]] == 0:
        cell_coords = [W, C]
    elif paint_grid[mid_right[0]][mid_right[1]] == 0:
        cell_coords = [E, C]
    elif paint_grid[bot_mid[0]][bot_mid[1]] == 0:
        cell_coords = [S, C]
    else:
        cell_coords = [C]
    #duplicate removal
    #cell_coords = list(set(cell_coords))
    return cell_coords

def paint_bg_rectangle(cells_list):
    #First we must find the scope of the cells, i.e. left,right,top,bottom extents
    left = cells_list[0][1]
    right = cells_list[0][1]
    top = cells_list[0][0]
    bottom = cells_list[0][0]
    for i in cells_list:
        left = min(left, i[1])
        right = max(right, i[1])
        top = min(top, i[0])
        bottom = max(bottom, i[0])
    hor_coords = list(range(2*left + 1, 2*right + 2))
    ver_coords = list(range(2*top + 1, 2*bottom + 2))
    for s in ver_coords:
        for t in hor_coords:
            paint_grid[s][t] = 1
    hor_border = list(range(2*left, 2*right + 3))
    ver_border = list(range(2*top, 2*bottom + 3))
    for s in ver_border:
        paint_grid[s][2*left] = 2
        paint_grid[s][2*right + 2] = 2
    for t in hor_border:
        paint_grid[2*top][t] = 2
        paint_grid[2*bottom + 2][t] = 2

while list_of_unpainted_bg_coords != []:
    cell = random.choice(list_of_unpainted_bg_coords)
    cells_to_paint = find_big_unpainted_rectangle(cell)
    for i in cells_to_paint:
        try:
            list_of_unpainted_bg_coords.remove(i)
        except ValueError:
            pass
    paint_bg_rectangle(cells_to_paint)


#Next we create the actual image! First we'll create the column and row sizes.
image_col_widths = [0]*big_grid_size
for i in range(big_grid_size):
    if i%2 == 0:
        image_col_widths[i] = 5
    else:
        image_col_widths[i] = random.randint(30,60)
image_row_heights = [0]*big_grid_size
for i in range(big_grid_size):
    if i%2 == 0:
        image_row_heights[i] = 5
    else:
        image_row_heights[i] = random.randint(30,60)

total_width = sum(image_col_widths)
total_height = sum(image_row_heights)

#Next we create a list that consists of the actual image data (with all the correct numbers!)
#We'll iterate over a giant grid, in which the index (pixel) is converted to the correct cell in paint_grid.

cum_col_widths = [0]*big_grid_size
cum_row_heights = [0]*big_grid_size
for i in range(big_grid_size-1):
    cum_col_widths[i+1] = cum_col_widths[i] + image_col_widths[i]
    cum_row_heights[i+1] = cum_row_heights[i] + image_row_heights[i]

def img_to_grid(i,j):
    grid_column = 0
    grid_row = 0
    for s in range(big_grid_size):
        if cum_col_widths[s] <= i:
            grid_column = s
        if cum_row_heights[s] <= j:
            grid_row = s
    return [grid_row, grid_column]

def colour_choice(i,j):
    coordinates = img_to_grid(i,j)
    coord0 = coordinates[0]
    coord1 = coordinates[1]
    if paint_grid[coord0][coord1] == 1:
        return (255,255,255)
    elif paint_grid[coord0][coord1] == 2:
        return (0,0,0)
    elif paint_grid[coord0][coord1] == 3:
        return (255,0,0)
    elif paint_grid[coord0][coord1] == 4:
        return (0,0,255)
    elif paint_grid[coord0][coord1] == 5:
        return (255,255,0)
    elif paint_grid[coord0][coord1] == 6:
        return (255,0,0)
    else:
        return (0,0,0)

image_data = [0]*total_height
for s in range(total_height):
    image_data[s] = [0]*total_width

for j in range(total_height):
    for i in range(total_width):
        image_data[j][i] = colour_choice(i,j)

image_data = [item for sublist in image_data for item in sublist]
img = Image.new('RGB', (total_width, total_height))
img.putdata(image_data)
img.show()
img.save('image.png')
