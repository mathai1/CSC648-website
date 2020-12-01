######################################################################################
# THIS IS search BLUEPRINT for search result page
######################################################################################
from flask import Blueprint, render_template, request,session


def initSearch(db): 
    # initalize search blueprint
    search = Blueprint('search', __name__)

    ######################################################################################
    # Search route
    # Getting the searched data from the database and render template of the searched data
    ######################################################################################
    @search.route('/search', methods= ['GET' , 'POST'])
    def searchpage():
        if request.method == 'POST':
            # Getting data from search     
            category = request.form['filter']
            searchedData = request.form['searchedData']

            # Perform the search through the database
            postings = db.searchAPosting(category,searchedData)     
            lst = db.getPostingOrganizedData(postings)

            # Make sure to display thumbnail instead of original image
            for l in lst:
                s = l['image'].split("/")[-1]
                l['image'] = "media/" + s 
            # If find any result in search, display the max of result for filter 
            if lst :
                high = max([ l['price']for l in lst])
                # Rendering all the data from the database from search
                return render_template("search/search.html", data = lst, searchedData = searchedData, category = category, high = high)                
        return render_template("search/search.html" , message ="No search results")

    ######################################################################################
    # filter route
    # Getting the searched data and filterfrom the database and render template of the searched data
    ######################################################################################
    @search.route('/filter', methods= ['GET' , 'POST'])
    def filterpage():
        if request.method == 'POST':
            # Getting data in the filter from request 
            category =request.args['filter']
            searchedData =request.args['searchedData']

            # This will be a filtering price 
            if 'min' in request.args and 'max' in request.args :
                min = request.args['min']
                max = request.args['max']
                order = request.args['order']
                postings = db.getPostingbyPrice(min, max, order, searchedData, category)
                return render_template("search/search.html", data = postings, searchedData = searchedData, category = category, min = min , max =  max, order = order)
        return render_template("search/search.html")

    return search
