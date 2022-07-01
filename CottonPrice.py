import streamlit as st
import pandas as pd
from pymongo import MongoClient
import ssl
from PIL import Image

# client = pymongo.MongoClient("mongodb+srv://aidept:admin123@cluster0.wbbm2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
# db = client.Marketing
# collection = db.article

#client = MongoClient("mongodb+srv://admin:root123@cluster0.fygmw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
client = MongoClient("mongodb+srv://aidept:admin123@cluster0.wbbm2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
db = client.test
collection = client['CottonPriceArticles']['databeforeJune2018']

doc = collection.find_one({'Status':"Pending"})
id = doc.get("_id")
print(id)
query = {'_id':id}

prev_doc = list(collection.find({'Status':"Completed"}).sort('_id',1))

# title = prev_doc['Title']

prev_id = prev_doc[-1].get("_id")
#print(prev_doc[-1].get("Title"))

prev_query = {'_id':prev_id}

img = Image.open("rtknits.png")

# display image using streamlit
# width is used to set the width of an image
col1, mid, col2 = st.columns([6,1,1])
with col2:
    st.image(img, width=200)

st.write("""
# News on Cotton Price
""")


countCompleted = collection.find({'Status':"Completed"}).count()
All = collection.find().count()

left_column, middle_col, right_column = st.columns([5,1,2])
back = st.button("Back")

hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden;}
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)

def getCount(right_column,countCompleted,All):
    with right_column:
        y = st.success("**{}/{}**".format(countCompleted,All))
    return y


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 175%;
min-height: 100%
background-color: dark;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; text-align: center;'target="_blank">The AI Department</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)


while back != True:
    with left_column:
        st.write("### Title")
        st.write(doc.get("Title"))
        st.write("### Description")
        st.write(doc.get("Description"))
        url = doc.get("Url")
        st.write("Click on the [Link](%s) for more" % url)
        st.write("##### Source")
        st.write(doc.get("Sources"))

    with right_column:
        st.write("##### Date")
        st.write(doc.get("Last Updated"))
        b1 = st.button('Potential Increase', key ='1')
        b2 = st.button('Potential Decrease', key ='2')
        b3 = st.button('Likely Stable', key ='3')
        b4 = st.button('Irrelevant', key ='4')

    if b1:
        collection.update_one(query,{"$set":{'Status': "Completed", 'Level': "Potential Increase"}})
        getCount(right_column,countCompleted,All)

    elif b2:
        collection.update_one(query,{"$set":{'Status': "Completed", 'Level': "Potential Decrease"}})
        getCount(right_column,countCompleted,All)

    elif b3:
        collection.update_one(query,{"$set":{'Status': "Completed", 'Level': "Likely Stable"}})
        getCount(right_column,countCompleted,All)

    elif b4:
        collection.update_one(query,{"$set":{'Status': "Completed", 'Level': "Irrelevant"}})
        getCount(right_column,countCompleted,All)

    break

else:
    with left_column:
        st.write("### Title")
        st.write(prev_doc[-2].get("Title"))
        st.write("### Description")
        st.write(prev_doc[-2].get("Description"))
        url = prev_doc[-2].get("Url")
        st.write("Click on the [Link](%s) for more" % url)
        st.write("##### Source")
        st.write(prev_doc[-2].get("Sources"))




    with right_column:
        st.write("##### Date")
        st.write(prev_doc[-2].get("Last Updated"))
        st.write(" ")
        b6 = st.button('Potential Increase', key ='6')
        b7 = st.button('Potential Decrease', key ='7')
        b8 = st.button('Likely Stable', key ='8')
        b9 = st.button('Irrelevant', key ='9')
        choice = st.write("You chose "+ prev_doc[-2].get("Level"))

    if b6:
        collection.update_one(prev_query,{"$set":{'Status': "Completed", 'Level': "Potential Increase"}})

    elif b7:
        collection.update_one(prev_query,{"$set":{'Status': "Completed", 'Level': "Potential Decrease"}})

    elif b8:
        collection.update_one(prev_query,{"$set":{'Status': "Completed", 'Level': "Likely Stable"}})

    elif b9:
        collection.update_one(prev_query,{"$set":{'Status': "Completed", 'Level': "Irrelevant"}})


#
#     with right_column:
#         b1 = st.button('High', key ='1')
#         b2 = st.button('Medium', key ='2')
#         b3 = st.button('Low', key ='3')
#         b4 = st.button('Not enough Info', key ='4')
#         b5 = st.button('Irrelevant', key='5')
#
#     if b1:
#         collection.update_one(query,{"$set":{'Status': "Completed", 'Level': "High"}})
#
#     elif b2:
#         collection.update_one(query,{"$set":{'Status': "Completed", 'Level': "Medium"}})
#
#     elif b3:
#         collection.update_one(query,{"$set":{'Status': "Completed", 'Level': "Low"}})
#
#     elif b4:
#         collection.update_one(query,{"$set":{'Status': "Completed", 'Level': "Not enough Info"}})
#
#     elif b5:
#         collection.update_one(query,{"$set":{'Status': "Completed", 'Level': "Irrelevant"}})

#
#     with right_column:
#         b6 = st.button('High', key ='6')
#         b7 = st.button('Medium', key ='7')
#         b8 = st.button('Low', key ='8')
#         b9 = st.button('Not enough Info', key ='9')
#         b10 = st.button('Irrelevant', key='10')
#         choice = st.write("You chose "+ prev_doc[-2].get("Level"))
#
#     if b6:
#         collection.update_one(prev_query,{"$set":{'Status': "Completed", 'Level': "High"}})
#
#     elif b7:
#         collection.update_one(prev_query,{"$set":{'Status': "Completed", 'Level': "Medium"}})
#
#     elif b8:
#         collection.update_one(prev_query,{"$set":{'Status': "Completed", 'Level': "Low"}})
#
#     elif b9:
#         collection.update_one(prev_query,{"$set":{'Status': "Completed", 'Level': "Not enough Info"}})
#
#     elif b10:
#         collection.update_one(prev_query,{"$set":{'Status': "Completed", 'Level': "Irrelevant"}})
