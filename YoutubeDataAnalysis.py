import pandas as pd
from googleapiclient.discovery import build

youTubeApiKey = "AIzaSyCQsoFj5a9ZHshYqQ8v7FPTB1wtOhe9m_s"
youtube = build('youtube','v3',developerKey=youTubeApiKey)
channelId='UCnc6db-y3IU7CkT_yeVXdVg' # J Cole's channel. You can take the channel ID of any channel of your choice

# Statistics
statdata=youtube.channels().list(part='statistics',id=channelId).execute()
print("Channel Stats: \n",statdata)
print("\n")

stats=statdata['items'][0]['statistics']
print("Stats: \n", stats)

print("\n")

videoCount=stats['videoCount']
print("Video Count",videoCount)

viewCount=stats['viewCount']
print("View Count: ", viewCount)

suscriberCount=stats['subscriberCount']
print("Number of Subscribers: ", suscriberCount)

# Snippet
snippetdata=youtube.channels().list(part='snippet',id=channelId).execute()
print("Basic info of the channel: \n", snippetdata)

title=snippetdata['items'][0]['snippet']['title']
print("Name of the Channel: ", title)

description=snippetdata['items'][0]['snippet']['description']
print("Description of the channel: \n", description)

logo=snippetdata['items'][0]['snippet']['thumbnails']['default']['url']
print("Channel logo url: ", logo)

# Content Details
contentdata=youtube.channels().list(id=channelId,part='contentDetails').execute()
playlist_id = contentdata['items'][0]['contentDetails']['relatedPlaylists']['uploads']
videos = []
next_page_token = None

while 1:
    res = youtube.playlistItems().list(playlistId=playlist_id,
                                    part='snippet',
                                    maxResults=50,
                                    pageToken=next_page_token).execute()
    videos += res['items']
    next_page_token = res.get('nextPageToken')

    if next_page_token is None:
        break

print("All video details: \n", videos)

video_ids = list(map(lambda x:x['snippet']['resourceId']['videoId'], videos))
print("Video ids: \n", video_ids)

stats = []
for i in range(0, len(video_ids), 40):
    res = (youtube).videos().list(id=','.join(video_ids[i:i+40]),part='statistics').execute()
    stats += res['items']

print("Stats for each video: \n", stats)

title=[]
liked=[]
disliked=[]
views=[]
url=[]
comment=[]
for i in range(len(videos)):
        title.append((videos[i])['snippet']['title'])
        url.append("https://www.youtube.com/watch?v="+(videos[i])['snippet']['resourceId']['videoId'])
        liked.append(int((stats[i])['statistics']['likeCount']))
        disliked.append(int((stats[i])['statistics']['dislikeCount']))
        views.append(int((stats[i])['statistics']['viewCount']))
        comment.append(int((stats[i])['statistics']['commentCount']))

data={'title':title,'url':url,'liked':liked,'disliked':disliked,'views':views,'comment':comment}
df=pd.DataFrame(data)
print("Table: \n", df)

# Analysis of data
print("Total number of videos uploaded on the channel: "+str(df.shape[0]))

print("Unique value of Video views: \n",df['views'].value_counts())

print("Unique value of Video likes: \n", df['liked'].value_counts())

print("Unique value of Video comments: \n", df['comment'].value_counts())

print("Unique value of Video dislikes: \n", df['disliked'].value_counts())

print("\n",df['liked'].isnull().value_counts())
print("Information: \n")
df.info()
print("Brief summary of the videos: \n")
print(df.describe())

print("Maxium number of likes on videos are: ",df['liked'].max())
print("Maxium number of dislikes on videos are: ",df['disliked'].max())
print("Maxium number of view on videos are: ",df['views'].max())
print("Maxium number of comments on videos are: ",df['comment'].max())

data_liked = df.sort_values(by = 'liked',axis = 0,ascending = True,ignore_index=True)
print("First 5 recent videos: \n")
print(df.head())
print(data_liked.head())

# count of unique values of videos i.e. count of likes,dislikes etc. using value_counts
print(df['liked'].value_counts(ascending = True,bins = 10))

print(df['disliked'].value_counts(ascending= True, bins = 10))

print(data_liked['disliked'].value_counts())

print(df['comment'].value_counts(ascending = True))

most_likedID = df['liked'].idxmax()
most_viewdID = df['views'].idxmax()
most_commentID = df['comment'].idxmax()
most_dislikedID = df['disliked'].idxmax()

print("Most liked video: \n",df.iloc[most_likedID].head)
print("Most viewed video: \n", df.iloc[most_viewdID].head)
print("Most commented video: \n", df.iloc[most_commentID].head)
print("Most disliked video: \n", df.iloc[most_dislikedID].head)

least_likedID = df['liked'].idxmin()
least_viewdID = df['views'].idxmin()
least_commentID = df['comment'].idxmin()
least_dislikedID = df['disliked'].idxmin()

print("Least liked video: \n",df.iloc[least_likedID].head)
print("Least viewed video: \n", df.iloc[least_viewdID].head)
print("Least commented video: \n", df.iloc[least_commentID].head)
print("Least disliked video: \n", df.iloc[least_dislikedID].head)
