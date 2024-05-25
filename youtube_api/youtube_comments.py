from googleapiclient.discovery import build
import googleapiclient.errors
from tqdm import tqdm
import pandas as pd
import traceback
import copy

def get_comment_threads(youtube, video_id, nextPageToken):
    results = youtube.commentThreads().list(
        part='snippet, replies',
        maxResults=100,
        videoId=video_id,
        textFormat="plainText",
        pageToken = nextPageToken
    ).execute()
    return results


class YouTubeComments():
    def __init__(self, video_id, youtube):
        self._null_data ={"author_name":[], "text":[], "reply_count":[], \
           "top_level":[], "index":[], "publishedAt":[], "updateAt"   :[], \
               "likeCount":[]}
        self._data = None
        self._video_id = video_id
        self._youtube = youtube
        self.next_page_token = ""
        self.token_reply = ""
        self.error = 0
        self._data = copy.copy(self._null_data)

    def _append_row(self, item, res, j, reply_count, top_level):
        author = item["snippet"]["authorDisplayName"]
        publishedAt = item["snippet"]["publishedAt"]
        updatedAt = item["snippet"]["updatedAt"]
        likeCount = item["snippet"]["likeCount"]
        text = item["snippet"]["textDisplay"]

        res["author_name"].append(author)
        res["text"].append(text)
        res["reply_count"].append(reply_count)
        res["top_level"].append(top_level)
        res["index"].append(j)
        res["publishedAt"].append(publishedAt)
        res["updateAt"].append(updatedAt)
        res["likeCount"].append(likeCount)

    def _add_data(self, match, j, res, youtube):
        for item in tqdm( match['items']):
            comment = item["snippet"]["topLevelComment"]

            reply_count = item['snippet']['totalReplyCount']
            self._append_row(comment, res, j, reply_count, 0)
            # if reply is there
            if reply_count>0:
                i = 1
                replies_list = youtube.comments().list(part='snippet',\
                                           maxResults=100, \
                                           parentId=item['id']).execute()
                for reply in replies_list['items']:
                    self._append_row(reply, res, j, reply_count, i)
                    i += 1

                while "nextPageToken" in  item['replies']['comments']:
                    self._token_reply =  item['replies']['nextPageToken']
                # get next set of 100 replies
                    replies_list = youtube.comments().list(part = 'snippet', \
                                               maxResults = 100, \
                                               parentId = item['id'], \
                                               pageToken = self.token_reply).execute()
                    for reply in replies_list['items']:
                    # add reply to list
                       self._append_row(reply, res, j, reply_count, i)
                       i += 1
            j += 1

        return j

    def _load_data(self):
        self._data = copy.copy(self._null_data)
        match = get_comment_threads(self._youtube, self._video_id, '')
        n = 0
        while match:
            n = self._add_data(match, n, self._data, self._youtube)
            if 'nextPageToken' in match:
                self.next_page_token = match["nextPageToken"]
                match = get_comment_threads(self._youtube, self._video_id, \
                                                          self.next_page_token)
            else:
                break


    def download_comments(self):
        try:
            self._load_data()
        except googleapiclient.errors.HttpError as err:
            self._error = err.resp.status
            print(f"HTTP ERROR STATUS: {self._error}")
            traceback.print_exc()
        return


    def get_df(self):
        return pd.DataFrame(self._data)

    def error(self):
        return self._error


def get_you_tube_comm(video_id, file_name):
    if __name__ == "__main__":

        youtube = build('youtube','v3',
                         developerKey='AIzaSyC2GjtdTC3-g6h1z-BvvhiMRQpLV6uJ04c')

        you_tube_comm = YouTubeComments(youtube=youtube, video_id=video_id)
        you_tube_comm.download_comments()
        return you_tube_comm.get_df().to_csv(file_name)

def get_video_transcript(video_id):
  subtitle_languages = get_subtitle_ids(video_id)
  if subtitle_languages:
    for language_code in subtitle_languages:
      subtitle_text = get_subtitle_text(video_id, language_code)
      if subtitle_text:
        transcript = process_subtitles(subtitle_text)
        print(f"Transcript for language {language_code}:")
        print("\n".join(transcript))
  else:
    print("No subtitles found for the video.")



    
if __name__ == "__main__":
    #get_you_tube_comm('Q8dc4A77gtY', 'blog_vid_5')

    video_id = "YOUR_VIDEO_ID_HERE"
    get_video_transcript(video_id)