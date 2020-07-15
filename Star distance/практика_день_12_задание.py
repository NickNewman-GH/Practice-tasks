import socket
import numpy as np
import matplotlib.pyplot as plt
import struct

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def star_outside(width, height):
    check = True
    count = 0
    while (pos[0]+count != img.shape[0] and pos[1]+count != img.shape[1] and pos[0]-count != 0 and pos[1]-count != 0 and img[pos[0]+count][pos[1]] != 0 and 
           img[pos[0]-count][pos[1]] != 0 and img[pos[0]][pos[1]+count] != 0 and img[pos[0]][pos[1]-count] != 0 and check == True):
        if img[pos[0]+count][pos[1]] == img[pos[0]-count][pos[1]]:
            width += 1
        else:
            check = False
        if img[pos[0]][pos[1]+count] == img[pos[0]][pos[1]-count]:
            height += 1
        else:
            check = False
        if img[pos[0]+count][pos[1]+count] == img[pos[0]-count][pos[1]-count]:
            height += 0.5
            width += 0.5
        else:
            check = False
        if img[pos[0]+count][pos[1]-count] == img[pos[0]-count][pos[1]+count]:
            height += 0.5
            width += 0.5
        else:
            check = False
        count += 1
    size[0] = width
    size[1] = height
    return check


host = "84.237.21.36"
port = 5152

plt.ion()
plt.figure()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))

    beat = b"nope"
    
    while beat != b"yep":

        sock.send(b"get")
        bts = recvall(sock, 40002)

        img = np.frombuffer(bts[2:], dtype="uint8").reshape(bts[0], bts[1])
        
        a=np.argmax(img)
        pos = np.unravel_index(a, img.shape)

        width = 1
        height = 1
        size = [width, height]
        pixel_colors = []
        if star_outside(width, height):
            for i in range(int(size[0]/2)):
                pixel_colors.append([])
                for j in range(int(size[1]/2)):
                    pixel_colors[i].append(img[pos[0]-int(size[0]/4)+i][pos[1]-int(size[1]/4)+j])
                    img[pos[0]-int(size[0]/4)+i][pos[1]-int(size[1]/4)+j] = 0            
            next_pos = np.unravel_index(np.argmax(img), img.shape)
            for i in range(int(size[0]/2)):
                for j in range(int(size[1]/2)):
                    img[pos[0]-int(size[0]/4)+i][pos[1]-int(size[1]/4)+j] = pixel_colors[i][j]
        else:
            count = 1
            while(1):
                    if (img[pos[0]+count][pos[1]] < img[pos[0]+count-1][pos[1]] and img[pos[0]-count][pos[1]] < img[pos[0]-count+1][pos[1]] and
                       img[pos[0]][pos[1]+count] < img[pos[0]][pos[1]+count-1] and img[pos[0]][pos[1]-count] < img[pos[0]][pos[1]-count+1] and
                       img[pos[0]+count][pos[1]+count] < img[pos[0]+count-1][pos[1]+count-1] and img[pos[0]-count][pos[1]-count] < img[pos[0]-count+1][pos[1]-count+1] and
                       img[pos[0]-count][pos[1]+count] < img[pos[0]-count+1][pos[1]+count-1] and img[pos[0]-count][pos[1]+count] < img[pos[0]-count+1][pos[1]+count-1]):
                        count += 1
                    else:
                        break
            for i in range(count):
                pixel_colors.append([])
                for j in range(count):
                    pixel_colors[i].append(img[pos[0]-int(count/2)+i][pos[1]-int(count/2)+j])
                    img[pos[0]-int(count/2)+i][pos[1]-int(count/2)+j] = 0            
            next_pos = np.unravel_index(np.argmax(img), img.shape)
            for i in range(count):
                for j in range(count):
                    img[pos[0]-int(count/2)+i][pos[1]-int(count/2)+j] = pixel_colors[i][j]
        
        delta = np.abs(np.array(pos)-np.array(next_pos))
        res1 = np.sqrt((pos[0]-next_pos[0])**2+(pos[1]-next_pos[1])**2)
        res = np.sqrt(delta[0]*delta[0]+delta[1]*delta[1])
        res = round(res ,1)
        sock.send(f'{res}'.encode())
        print(sock.recv(20))

        plt.clf()
        plt.suptitle(f'delta = {str(delta)}, distance = {res}')
        plt.title(str(pos)+', '+str(next_pos))
        plt.imshow(img)

        plt.pause(0.00000001)

        sock.send(b"beat")
        beat = sock.recv(20)

print("Done!")

