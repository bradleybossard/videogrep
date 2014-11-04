import re # module for regular expressions

def convert_time(timestring):
    """ Converts a string into seconds """
    nums = map(float, re.findall(r'\d+', timestring))
    return 3600*nums[0] + 60*nums[1] + nums[2] + nums[3]/1000

with open("state_of_the_union/state.srt") as f:
    lines = f.readlines()

# Organize subtitles in more Python-friendly ([start_time, stop_time], 'text') object.
times_texts = []
current_times , current_text = None, ""
for line in lines:
    times = re.findall("[0-9]*:[0-9]*:[0-9]*,[0-9]*", line)
    if times != []:
        current_times = map(convert_time, times)
    elif line == '\n':
        times_texts.append((current_times, current_text))
        current_times, current_text = None, ""
    elif current_times is not None:
        current_text = current_text + line.replace("\n"," ")

#print (times_texts)

# Find ten most common words
from collections import Counter
whole_text = " ".join([text for (time, text) in times_texts])
all_words = re.findall("\w+", whole_text)
counter = Counter([w.lower() for w in all_words if len(w)>5])
print (counter.most_common(10))

# Get all the time segments containing the word "should"
cuts = [times for (times,text) in times_texts
        if (re.findall("should",text) != [])]


# Create a super cut of it.
from moviepy.editor import VideoFileClip, concatenate

video = VideoFileClip("state_of_the_union/state.mp4")

def assemble_cuts(cuts, outputfile):
    """ Concatenate cuts and generate a video file. """
    final = concatenate([video.subclip(start, end)
                         for (start,end) in cuts])
    final.to_videofile(outputfile)

assemble_cuts(cuts, "should.mp4")
