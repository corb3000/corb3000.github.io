import sqlite3
from sqlite3 import Error
import json
from pyscript import display, Element
from js import  document


houses = []
house_images = []
image_number = 0
house_count = 0



# Create all the event handlers

def get_connection():
    conn = None
    try:
        conn = sqlite3.connect("./houses.db")
        return conn
    except Error as e:
        print("DB open error",e)

def get_house_data():
    cur = c.cursor()
    cur.execute("""SELECT DISTINCT property_type FROM house """)   
    type = cur.fetchall()
    cur.execute("""SELECT DISTINCT county FROM house """)   
    county = cur.fetchall()
    countySel = document.getElementById('daySelect')
    d = Element("choose_county")
    d.element.innerHTML = ""
    # d.element.innerHTML =f'<option value="all">all</option>'
    for i in county:
        d.element.innerHTML += f'<option value="{i[0]}">{i[0]}</option>'
    

   

def select_data():
    cur = c.cursor()
    search = Element('desc_search')
    search_ = f"%{search.value}%"
    den = Element('pop-dty')
    min_price = Element('min_price')
    max_price = Element('max_price')
    bed = Element('min_bed')
    cty = Element('choose_county')
    county = cty.element.selectedOptions
    ob = Element('orderBy')
    orderBy = ob.value


    # c=county.element.selectedOptions
    if county.length == 0:
        county = cty.element.options
    cl= []
    for i in range(county.length):
        cl.append(county.item(i).value)
    sql = 'SELECT * FROM house WHERE county IN ({}) AND description LIKE ? AND price BETWEEN ? AND ? AND bedrooms > ? AND density_3k < ? ORDER BY {} '.format(','.join(['?']*len(cl)), orderBy)
    cl = cl+[search_ , min_price.value, max_price.value, bed.value, den.value]
    cl = tuple(cl)
    cur.execute(sql, cl)
     
    rows_all = cur.fetchall()
    if rows_all:
        houses.clear()
        houses.extend(rows_all)
        global house_count 
        house_count = 0
        display_house()


def display_house():
    # global houses
    global house_count
    global image_number
    house_images.clear()
    Element("house_count").write(house_count + 1)
    Element("house_len").write(len(houses))
    house_count = max(house_count,0)
    house_count = min(house_count,len(houses)-1)
    image_number = 0
    house = houses[house_count]
    images = house[13]
    description = house[5] 
    row = json.loads(images)
    house_images.extend(row)
    image1 = row[image_number]
    url1 = image1["srcUrl"]
    caption = image1["caption"]
    Element("caption").write(caption)
    Element('address').write(house[7])
    Element('price').write(f"  ${int(house[6])}")
    Element('bed').write(int(house[1]))
    # Element('bath').write(int(house[2]))
    Element('county').write(house[14])
    Element('type').write(house[4])
    # Element('listingUpdateDate').write(house[11])
    Element('den_1').write(int(house[15]))
    Element('den_2').write(int(house[16]))
    Element('den_5').write(int(house[17]))
    Element("description").write(description)
    document.querySelector("img").setAttribute("src", url1)
    link = f"https://www.rightmove.co.uk{house[10]}"
    l = document.getElementById("property")
    l.setAttribute("href", link)
    l.setAttribute("target", "_blank")
    l = document.getElementById("prop_image")
    l.setAttribute("href", link)
    l.setAttribute("target", "_blank")   

def back_handler():
    row = house_images
    global image_number
    image_number -= 1
    if image_number < 0:
        image_number = max(len(row)-1,0)
    image1 = row[image_number]
    url1 = image1['srcUrl']
    caption = image1["caption"]
    Element("caption").write(caption)
    document.querySelector("img").setAttribute("src", url1)


def next_handler():
    row = house_images
    global image_number
    image_number += 1
    if image_number > len(row)-1:
        image_number = 0
    image1 = row[image_number]
    caption = image1["caption"]
    Element("caption").write(caption)
    url1 = image1['srcUrl']
    document.querySelector("img").setAttribute("src", url1)

def house_back_handler():
    global house_count
    house_count -= 1
    Element("house_count").write(house_count + 1)
    display_house()

def house_next_handler():
    global house_count
    house_count += 1
    Element("house_count").write(house_count + 1)
    display_house()

c = get_connection()
get_house_data()
select_data()