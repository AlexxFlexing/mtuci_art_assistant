import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import extcolors
from colormap import rgb2hex
from PIL import Image #rendering image/opening image

def img_to_palette(img):
    #input_image_name = file_path               
    output_image_width = 900                  #set the output size
    #img = Image.open(input_image_name)        
    w_percent = (output_image_width/float(img.size[0]))
    h_size = int((float(img.size[1])*float(w_percent)))
    img = img.resize((output_image_width,h_size), Image.LANCZOS)  # resize the image
    #save

    #fix .jpeg(non)
    #resize_name = input_image_name[:-4].replace('input','output',1) +'_resized'+ '.jpg'  # save resized image
    #img.save(f'C:/Users/aleks/Desktop/step2/output/palette_temp/{resize_name}')                 
    #read
    plt.figure(figsize=(9, 9))  
    #img_url = f'C:/Users/aleks/Desktop/step2/output/palette_temp/{resize_name}'       

    tolerance_param = 13
    limit_param = 13
    colors_extracion = extcolors.extract_from_image(img, tolerance = tolerance_param, limit = limit_param)  # extract colors for later use
    #colors_extracion #not needed??????
    #color to dataframe
    def color_to_df(input): # now convert extracted colos into dataframe 
        colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
        df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
        df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
        #convert RGB to HEX code
        df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                        int(i.split(", ")[1]),
                        int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
        df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
        return df
    df_color = color_to_df(colors_extracion)
    df_color # dataframe
    #donutchart color analisys 
    list_color = list(df_color['c_code'])
    list_precent = [int(i) for i in list(df_color['occurence'])]
    text_c = [c + ' ' + str(round(p*100/sum(list_precent),1)) +'%' for c, p in zip(list_color, list_precent)]    
    fig1, ax1 = plt.subplots(figsize=(90,90),dpi=10)
    wedges, text = ax1.pie(list_precent,
                        labels= text_c,
                        labeldistance= 1.05,
                        colors = list_color,
                        textprops={'fontsize': 120, 'color':'black'}
                        )
    plt.setp(wedges, width=0.3)
    #create space in the center
    plt.setp(wedges, width=0.36)
    ax1.set_aspect("equal")
    fig1.set_facecolor('white')
    plt.savefig("C:/Users/aleks/Desktop/step2/output/palette_donut.png")
    #color palette
    
    fig, ax = plt.subplots(figsize=(72,57.6),dpi=10)
    fig.set_facecolor('white')        #create background color
    plt.savefig("C:/Users/aleks/Desktop/step2/output/palette_temp/bg.png")
    plt.close(fig)
    #create color palette
    bg = plt.imread("C:/Users/aleks/Desktop/step2/output/palette_temp/bg.png")
    fig = plt.figure(figsize=(72,57.6), dpi = 10) 
    ax = fig.add_subplot(1,1,1)
    color_json = {}
    color_number = 0
    x_posi, y_posi, y_posi2 = 0, 0, 0
    for c in list_color:   #adjusting position of a color inside color palette
        if list_color.index(c) == 0:
            y_posi = 0
            rect = patches.Rectangle((x_posi, y_posi), 360, 96, facecolor = c)
            ax.add_patch(rect)
        elif  list_color.index(c) <= 5 and list_color.index(c) != 0:
            y_posi += 96

            rect = patches.Rectangle((x_posi, y_posi), 360, 96, facecolor = c)
            ax.add_patch(rect)
        elif list_color.index(c) == 6:
            y_posi2 += 0
            rect = patches.Rectangle((x_posi + 360, y_posi2), 360, 96, facecolor = c)
            ax.add_artist(rect)
        else:
            y_posi2 += 96
            rect = patches.Rectangle((x_posi + 360, y_posi2), 360, 96, facecolor = c)
            ax.add_artist(rect)
        color_json.update({f'color{color_number}': f'{c}'})
        color_number +=1
    ax.axis('off')
    fig.set_facecolor('white')
    plt.imshow(bg, alpha=0.1)       
    plt.tight_layout()
    plt.savefig("C:/Users/aleks/Desktop/step2/output/palette_rectangles.png")
    return color_json
    #print(color_json)                                   
    
