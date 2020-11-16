# THIS IS Posting BLUEPRINT for posting page
#retriveing a posting 
# /posting/<postingid>
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

def initPost(db) :
    posting = Blueprint('posting', __name__)

    @posting.route('/posting/<postid>')
    def getPost(postid):
        post = db.getAPosting("postID", postid)
        posts = db.getPostingOrganizedData(post)
        return render_template("posting/posting.html", posting = posts[0] )

    @posting.route('/posting', methods=['GET', 'POST'])
    def createPost():
        if request.method == "POST":
            file = request.files['img']
            filename = secure_filename(file.filename)
            path = f'static/images/postings/{filename}'
            file.save(path)
            db.createThumbnail( path,f'static/media/{filename}')
            print("Done")
    
        return render_template("posting/create.html")

    

        
    return posting