import csv
import pandas as pd
import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import norm
import sklearn.preprocessing as pp
from IPython.display import display
from math import sqrt

np.set_printoptions(threshold=500, precision=4)
pd.options.display.max_seq_items = 100
# %precision 4

# %load_ext autoreload
# %autoreload 2

data_location = 'ratings.csv' ## location of ratings.csv
ratings_raw = pd.read_csv(data_location)
DEBUG = True
if DEBUG: 
    ratings_raw = ratings_raw[ (ratings_raw['userId'] < 10000) & (ratings_raw['movieId'] < 1000) ]

# display(ratings_raw.head())

movieIds = ratings_raw.movieId.unique()
movieIds.sort()
userIds = ratings_raw.userId.unique()
userIds.sort()

m = userIds.size
n = movieIds.size
numRatings = len(ratings_raw)

# print ("There are", m, "users,", n, "items and", numRatings, "ratings.")

## create internal ids for movies and users, that have consecutive indexes starting from 0
movieId_to_movieIDX = dict(zip(movieIds, range(0, movieIds.size)))
movieIDX_to_movieId = dict(zip(range(0, movieIds.size), movieIds))

userId_to_userIDX = dict(zip(userIds, range(0, userIds.size )))
userIDX_to_userId = dict(zip(range(0, userIds.size), userIds))

## drop timestamps
ratings = pd.concat([ratings_raw['userId'].map(userId_to_userIDX), ratings_raw['movieId'].map(movieId_to_movieIDX), ratings_raw['rating']], axis=1)
ratings.columns = ['user', 'item', 'rating']

# display(ratings.head())

R = sp.csr_matrix((ratings.rating, (ratings.user, ratings.item)))
R_dok = R.todok()

m = R.shape[0]
n = R.shape[1]
numRatings = R.count_nonzero()

# print("There are", m, "users,", n, "items and", numRatings, "ratings.")
















#THE FUN STARTS HERE!!!

user_sums = R.sum(axis=1).A1 ## matrix converted to 1-D array via .A1
user_cnts = (R != 0).sum(axis=1).A1
user_avgs = user_sums / user_cnts
# print("user_avgs", user_avgs)
def compute_pairwise_user_similarity(u_id, v_id):
    """
    This function takes two user IDs as an input and computes their pairwise similarity.

    :return: mean-centered cosine similarity score
    :rtype: float
    """

    u = R[u_id,:].copy()
    v = R[v_id,:].copy()
    
    # YOUR CODE HERE

    umat=u.toarray()
    vmat=v.toarray()
    umat=umat[0]
    vmat=vmat[0]

    uavg= user_avgs[u_id]
    vavg=user_avgs[v_id]
    den_u = 0
    den_v = 0
    numerator= 0
    
    for i in range(0,len(movieIds)):
        if umat[i]!=0:
            den_u+=(float(umat[i])-float(uavg))**2
        if vmat[i]!=0:
            den_v+=(float(vmat[i])-float(vavg))**2
        if umat[i]>0 and vmat[i]>0:
            numerator+=((umat[i]-uavg)*(vmat[i]-vavg))
    denominator=(den_u**(1/2))*(den_v**(1/2))

    if denominator == 0:
        similarity = 0.;
    else:
        similarity = round(numerator/denominator, 4)
    
    return similarity

# if DEBUG:
#     display(compute_pairwise_user_similarity(2, 6))


















def compute_user_similarities(u_id, R=R, user_avgs=user_avgs, user_cnts=user_cnts):
    """
    This function takes a user ID as an input and computes the pairwise similarity to all other users.
    
    :return:Similarity vector of the user to all others (shape: (m, ))
    :rtype: numpy.ndarray
    """
    uU = np.empty((m,))

    # YOUR CODE HERE
    uU=np.ndarray((m, ), dtype=float)
    for i in range(0, len(user_avgs)):
        uU[i] = float(compute_pairwise_user_similarity(u_id, i))
    return uU

# if DEBUG:
#     uU = compute_user_similarities(2)
#     display(uU[6])

















# default values
k = 5
with_abs_sim = False
def absolute_dictionary(dicty):
    newdicty = {}
    for key, value in dicty.items():
        if value<0 or key<0:
            value = -value
            key = -key
        newdicty[key] = value
    return newdicty

def create_user_neighborhood(u_id, i_id,compute_user_similarities=compute_user_similarities, R=R, R_dok=R_dok, user_avgs=user_avgs, user_cnts=user_cnts):
    nh = {}
    uU = compute_user_similarities(u_id, R, user_avgs, user_cnts)
    uU_copy = uU.copy()
    
    # YOUR CODE HERE
    temporary_dict={}
    for i in range(0, len(user_avgs)):
        if (i, i_id) in R_dok:
            if i != u_id:
                temporary_dict[i] = uU_copy[i]
    if with_abs_sim == False:
        temporary_dict = dict(sorted(temporary_dict.items(), key=lambda item: item[1], reverse=True))
    else: 
        temporary_dict = absolute_dictionary(temporary_dict)
        temporary_dict = dict(sorted(temporary_dict.items(), key=lambda item: item[1], reverse=True))
    
    n=0
    if with_abs_sim == True:
        temporary_dict=absolute_dictionary(temporary_dict)
    for key, value in temporary_dict.items():
        if n > 4:
            break
        nh[key] = value
        n+=1
    nh = dict(sorted(nh.items(), key=lambda item: item[0]))
        
    
    return nh

if DEBUG:
    k = 5
    with_abs_sim = False
    nh = create_user_neighborhood(0, 8)
    print("with_abs_sim", with_abs_sim)
    display(nh)
    with_abs_sim = True
    nh = create_user_neighborhood(0, 8)
    print("with_abs_sim", with_abs_sim)
    display(nh)




# def create_user_neighborhood(u_id, i_id,compute_user_similarities=compute_user_similarities, R=R, R_dok=R_dok, user_avgs=user_avgs, user_cnts=user_cnts):
#     """
#     This function takes a user ID as an item ID as input and calculates the neighborhood of size k.
    
#     :return: neighborhood dictionary (user id: similarity) with k entries
#     :rtype: dict[int,float]
#     """
#     nh = {} ## the neighborhood dict with (user id: similarity) entries
#     ## nh should not contain u_id and only include users that have rated i_id; there should be at most k neighbors
#     uU = compute_user_similarities(u_id, R, user_avgs, user_cnts)
#     uU_copy = uU.copy() ## so that we can modify it, but also keep the original
    
#     # YOUR CODE HERE
#     newdict={}
#     absolutedict = {}
#     for i in range(0, len(user_avgs)):
#         if (i, i_id) in R_dok:
#             if i != u_id:
#                 newdict[i] = uU_copy[i]
#     if with_abs_sim == False:
#         newdict = dict(sorted(newdict.items(), key=lambda item: item[1], reverse=True))
#     else: 
#         for key, value in newdict.items():
#             if value<0:
#                 value = value*(-1)
#                 key = key*(-1)
#             absolutedict[key] = value
#         absolutedict = dict(sorted(absolutedict.items(), key=lambda item: item[1], reverse=True))
    
#     n=0
#     if with_abs_sim == False:
#         for key, value in newdict.items():
#             if n > 4:
#                 break
#             nh[key] = value
#             n+=1
#         nh = dict(sorted(nh.items(), key=lambda item: item[0]))
#     else: 
#         newdict = {}
#         for key, value in absolutedict.items():
#             if key<0:
#                 value = value*(-1)
#                 key = key*(-1)
#             newdict[key] = value
#         for key, value in newdict.items():
#             if n > 4:
#                 break
#             nh[key] = value
#             n+=1
#         nh = dict(sorted(nh.items(), key=lambda item: item[0]))
            
    
#     return nh
















# ## a default value
# with_deviations = True

# def predict_rating(u_id, i_id, create_user_neighborhood = create_user_neighborhood, compute_user_similarities = compute_user_similarities):
#     """
#     This function takes a user ID and an item ID as an input and predicts the rating a user would give this item.
    
#     :return: predicted rating for the selected item
#     :rtype: float
#     """
    
#     if (u_id, i_id) in R_dok:
#         print("user", u_id, "has rated item", i_id, "with", R[u_id, i_id])
#     else:
#         print("user", u_id, "has not rated item", i_id)
#     print("k:", k, "with_deviations:", with_deviations, "with_abs_sim:", with_abs_sim)
    
    
#     nh = create_user_neighborhood(u_id, i_id,compute_user_similarities, R, R_dok, user_avgs, user_cnts, with_abs_sim, k)
    
#     neighborhood_weighted_avg = 0.

#     # YOUR CODE HERE
#     raise NotImplementedError()
    
#     if with_deviations:
#         prediction = user_avgs[u_id] + neighborhood_weighted_avg
#         print(f'prediction {prediction:.4f} (user_avg {user_avgs[u_id]:.4f} offset {neighborhood_weighted_avg:.4f})')
#     else:
#         prediction = neighborhood_weighted_avg
#         print(f'prediction {prediction:.4f} (user_avg {user_avgs[u_id]:.4f})')
        
#     return prediction

# if DEBUG:
#     k = 50
#     with_abs_sim = True
#     with_deviations = False
#     predict_rating(0, 8)
#     with_deviations = True
#     predict_rating(0, 8)

# k = 50
# with_deviations = True
# with_abs_sim = True
# predict_rating(0, 8)
# %time predict_rating(22, 35)

# print("done!")

# k = 50
# with_deviations = False
# with_abs_sim = False
# predict_rating(0, 12)
# %time predict_rating(22, 35)

# print("done!")
