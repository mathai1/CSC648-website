######################################################################################
# THIS IS Posting BLUEPRINT for posting page
#retriveing a posting 
# /posting/<postingid>
######################################################################################
from flask import Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename

def initPost(db) :
    posting = Blueprint('posting', __name__)


    ######################################################################################
    # Go directly to a posting route
    # Getting the postid and retriving the posting information based on the post id
    ######################################################################################
    @posting.route('/posting/<postid>')
    def getPost(postid):
        post = db.getAPosting("postID", postid)
        posts = db.getPostingOrganizedData(post)
        return render_template("posting/posting.html", posting = posts[0] )

    ######################################################################################
    # This is creating a post route 
    # Getting the data of posting from POST request and then store it into the database
    ######################################################################################
    @posting.route('/posting', methods=['GET', 'POST'])
    def createPost():
        if request.method == "POST":
            # Getting info from post and send to the database
            file = request.files['img']
            posting = {}
            data = request.form.to_dict()
            print(data)
            posting['title'] = data['title']
            posting['description'] = data['discription']
            posting['price'] = int(data['price'] ) 
            posting['category'] = data['filter']

            # Create thumbnails if user upload an image
            if file.filename != '' :       
                filename = secure_filename(file.filename) # Make sure file is sanitized from users
                path1 = f'static/images/postings/{filename}'
                path2 = f'images/postings/{filename}'
                file.save(path1)
                db.createThumbnail( path1,f'static/media/{filename}') #This method creating thumb nails and store it into media
                posting['image'] = path2
            else :
                posting['image'] = "images/postings/empty.png"

            # Send to the database
            db.insertAPosting(posting)
            return redirect("/")
    
        return render_template("posting/create.html")

    

        
    return posting