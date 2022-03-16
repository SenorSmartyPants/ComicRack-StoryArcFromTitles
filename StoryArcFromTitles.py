# StoryArcFromTitles.py
#
# Attempts to parse Titles to find Story Arc Info 
# 
#
# You are free to modify and distribute this file
##########################################################################

import clr
import System
import re

clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import *
#from System.Windows.Forms import DialogResult, MessageBox, MessageBoxButtons, MessageBoxIcon


import MethodForm
from MethodForm import MethodForm

GroupKeywords = ["Part","Chapter",": ","Pt.","Pt"]

NoStoryArcKey = "---***No Story Arc Found***---"
StoryArcMinimumLength = 6 # seems to be off by one... 
SingleStoryArcMinimumLength = 2

#@Name	Get Story Arcs from Titles...
#@Hook	Books
#@Description Get Story Arcs from Titles...
#@Image StoryArcFromTitles.png
def StoryArcFromTitles(books):
	#test to make sure there is more than one book
	if len(books) == 0:
		MessageBox.Show("You must select at least 1 book to run this script", "Story Arc From Titles", MessageBoxButtons.OK, MessageBoxIcon.Warning)

	elif len(books) == 1:
		#MessageBox.Show("You must select at least 2 books to run this script", "Story Arc From Titles", MessageBoxButtons.OK, MessageBoxIcon.Warning)
		
		#single story arc mode - only one book
		SingleStoryArcFromTitles(books)
	
	else:
		method_form = MethodForm()
		if (method_form.ShowDialog() == DialogResult.OK):
			#MessageBox.Show("dialog ok result")
			method_selected = method_form._cblMethod.SelectedIndex			#MessageBox.Show(method_form._cblMethod.SelectedIndex.ToString())

			if method_selected == 0 or method_selected == 1:
				MultipleStoryArcsFromTitles(books,method_selected)
			else:
				#single story arc mode
				SingleStoryArcFromTitles(books)
	
def SingleStoryArcFromTitleArray(titleArray):
	#test based on number of books selected
	if len(titleArray) > 1:
		#more than 1 book
		storyarc = long_substr(titleArray)
	else:
		#only 1 book - remove part/chapter and everything after
		storyarc = removeGroupKeywordsAndAfter(titleArray[0])
		#MessageBox.Show(storyarc)
		#make sure story arc is not the same as the title
		if storyarc == titleArray[0]:
			storyarc = ""
	#endif
	if len(storyarc) < SingleStoryArcMinimumLength:
		storyarc = ""
	
	return storyArc_cleanup(storyarc)

def SingleStoryArcFromTitles(books):

	titleArray = makeTitleArray(books)
	storyarc = SingleStoryArcFromTitleArray(titleArray)
	
	if len(storyarc) == 0:
		MessageBox.Show("No Story Arcs detected.", "Story Arc From Titles", MessageBoxButtons.OK, MessageBoxIcon.Warning)
	else:
		#ask to overwrite if not empty
		#0 is cancel
		#1 is unchecked
		#2 is checked
		result = ComicRack.App.AskQuestion (
			ComicRack.Localize("StoryArcFromTitles", "Ask", "Possible Story Arc detected.\n" + storyarc + "\n\nDo you want to update selected books with the detected Story Arc?"), 
			ComicRack.Localize("StoryArcFromTitles", "Continue", "Continue"), 
			ComicRack.Localize("StoryArcFromTitles", "Overwrite", "&Overwrite existing story arcs"))

		#overwrite if checked or number is empty
		if result != 0:
			for book in books:		
				ProcessAlternateSeries(book,storyarc,result == 2)
#end SingleStoryArcFromTitles


def ProcessAlternateSeries(book,storyarc,overwrite):
	# if there is an alternate series and it is the same as the storyarc name, set alternate series number
	# find number after the groupkeyword, chapter/part number
	lstoryarc = storyarc.lower()
	lAlternateSeries = book.AlternateSeries.lower()
	#MessageBox.Show(lAlternateSeries.find(lstoryarc).ToString())
	if lAlternateSeries.find(lstoryarc) != -1 and lstoryarc != lAlternateSeries:
		RemoveStoryArcFromAlternateSeries(book,storyarc,overwrite)
	if lstoryarc != lAlternateSeries:
		if overwrite or book.StoryArc == "":
			if len(storyarc) > 0:
				book.StoryArc = storyarc
	else:
		#don't put found story arc in storyarc field since it is really an alternate series
		#TODO: check title again for another story arc?
		AlternateSeriesNumberHandling(book,storyarc,overwrite)

#end ProcessAlternateSeries
def RemoveStoryArcFromAlternateSeries(book,storyarc,overwrite):
	#remove story arc from AlternateSeries, save it in story arc
	#story arc could be one of several in AlternateSeries
	if overwrite:
		book.AlternateSeries = book.AlternateSeries.replace(storyarc,"").strip(' ,-(:;')
		
		
		
		#MessageBox.Show(re.sub(re.compile(re.escape(storyarc),re.I),"",book.AlternateSeries,0))
		
	#MessageBox.Show(book.AlternateSeries)
#end RemoveStoryArcFromAlternateSeries

def AlternateSeriesNumberHandling(book,storyarc,overwrite):
	#find a part number if it exists
	if len(book.AlternateSeries) > 0:
		#remove story arc from title
		PartNumber = book.Title.replace(storyarc,"").strip().lstrip(',-(:;').strip()
		#MessageBox.Show(PartNumber)
		#remove group keyword, if it exists find first word after it. 
		for Part in GroupKeywords:
			PartNumber = PartNumber.replace("(" + Part, " ")
			PartNumber = PartNumber.replace(Part, " ")
		#take first word left, use that as part number
		PartNumber = PartNumber.strip()
		#MessageBox.Show(PartNumber)
		#MessageBox.Show(PartNumber.find(" ").ToString())
		spaceIndex = PartNumber.find(" ")
		if spaceIndex > -1:
			PartNumber = PartNumber[:PartNumber.find(" ")]
		PartNumber = PartNumber.strip(',-(:;').strip()
		#MessageBox.Show("Alternate Series:\n" + book.AlternateSeries + " #" + PartNumber)
		
		if overwrite or len(book.AlternateNumber) == 0:
			#convert to integer, if error just use text
			try:
				book.AlternateNumber = text2int(PartNumber).ToString()
			except Exception:
				book.AlternateNumber = PartNumber
	
				
#end AlternateSeriesNumberHandling


def text2int(textnum, numwords={}):
	textnum = textnum.lower()
	
	if not numwords:
		units = [
		"zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
		"nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
		"sixteen", "seventeen", "eighteen", "nineteen",
		]

		tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

		scales = ["hundred", "thousand", "million", "billion", "trillion"]

		numwords["and"] = (1, 0)
		for idx, word in enumerate(units):    numwords[word] = (1, idx)
		for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
		for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)



	current = result = 0
	for word in textnum.split():
		if word not in numwords:
			raise Exception("Illegal word: " + word)

		scale, increment = numwords[word]
		current = current * scale + increment
		if scale > 100:
			result += current
			current = 0

	return result + current
	

def MultipleStoryArcsFromTitles(books,method_selected):

	titleArray = makeTitleArray(books)


	storyarcs = prefix_groups(titleArray,method_selected)

	if storyarcs:
		result = ComicRack.App.AskQuestion (
				ComicRack.Localize("StoryArcsFromTitles", "Ask", "Results of Story Arc scan\n" + formatDict(storyarcs)), 
				ComicRack.Localize("StoryArcsFromTitles", "Continue", "Continue"), 
				ComicRack.Localize("StoryArcsFromTitles", "Overwrite", "&Overwrite existing story arcs"))

		#overwrite if checked or number is empty
		if result != 0:
			
			#invert dictionary, so book title is now the key, story arc the value
			inv = {}
			for k, v in storyarcs.iteritems():
				if k != NoStoryArcKey:
					#print k
					for title in v:
						#print title
						inv[title] = k
			
			#print inv
			
			#update books
			for book in books:
				storyarc = ""
				if inv.has_key(book.Title):
					storyarc = inv[book.Title]

				ProcessAlternateSeries(book,storyarc,result == 2)
#end MultipleStoryArcsFromTitles

def makeTitleArray(books):
	titleArray = []
	for book in books:
		#print "%s V%d #%s" % (book.Series , book.Volume , book.Number)
		#print book.Title
		#print book.StoryArc
		titleArray.append(book.Title)
	
	print titleArray
	
	return titleArray		

#http://stackoverflow.com/questions/2892931/longest-common-substring-from-more-than-two-strings-python
# this does not increase asymptotical complexity
# but can still waste more time than it saves.
def shortest_of(strings):
    return min(strings, key=len)

def long_substr(strings):
	#case insensitive
    substr = ""
    if not strings:
        return substr
    reference = shortest_of(strings) #strings[0]
    length = len(reference)
    #find a suitable slice i:j
    for i in xrange(length):
        #only consider strings long at least len(substr) + 1
        for j in xrange(i + len(substr) + 1, length + 1):
            candidate = reference[i:j]  # is the slice recalculated every time?
            if all(candidate.lower() in text.lower() for text in strings):
                substr = candidate
    return substr
	
def prefix_groups(data,method):
	"""Return a dictionary of {prefix:[items]}."""
	lines = data[:]
	groups = dict()
	groups[NoStoryArcKey] = list()
	
	
	if method == 0:
		#remove part and everything after it from title
		removeP = removeGroupKeywordsAndAfter 
	elif method == 1:
		#use alternate Part removal, only remove the word Part from Title
		removeP = removeGroupKeywords
	else:
		#shouldn't call if method is not 0 or 1
		return
		
				
	while lines:
		longest = None
		first = lines.pop()
		
		
		firstNoPart = removeP(first)

		for line in lines:
			prefix = long_substr([firstNoPart, removeP(line)])
			prefix = storyArc_cleanup(prefix)
			#print firstNoPart + "|" + line + "|" + prefix
			if not longest:
				if len(prefix) >= StoryArcMinimumLength:
					#print len(prefix)
					longest = prefix
			elif len(prefix) > len(longest) and len(prefix) >= StoryArcMinimumLength:
				longest = prefix
			#if longest print "longest = " + longest
			#print "prefix = " + prefix

		if longest:
			#group = [first]
			rest = [item for item in lines if longest.lower() in item.lower()]
			#print "rest = " + str(rest)
			[lines.remove(item) for item in rest]
			rest.append(first)
			groups[longest] = rest
			#print "group found = " + longest
		else:
			# Singletons raise an exception
			#raise IndexError("No prefix match for {}!".format(first))
			#print "no Story Arc found for " + first
			#groups[NoStoryArcKey].append(first)
			
			#TODO: do single title check for possible story arc
			single = SingleStoryArcFromTitleArray([first])
			if len(single) == 0:
				groups[NoStoryArcKey].append(first)
			else:
				#should only ever be one title in this group
				groups[single] = list()
				groups[single].append(first)
			#MessageBox.Show(SingleStoryArcFromTitleArray([first]))

	#remove no story arc key if empty list
	if len(groups[NoStoryArcKey]) == 0:
		del groups[NoStoryArcKey]
	return groups


def formatDict(dictionary):
	output = ""
	for k, v in dictionary.items():
		output += k + "\n"
		for item in v:
			output += "\t   " + item + "\n"
		output += "\n"
	
	return output

	
	
def removeGroupKeywords(s):
	processedString = s
	for Part in GroupKeywords:
		processedString = removePart(processedString,Part)
	return processedString
	
def removePart(s,keyword):
	#don't add spaces if already space in keyword
	if keyword.find(" ") == -1:
		keyword = " " + keyword + " "
	partIndex = s.rfind(keyword)
	if partIndex != -1:
		#remove Part from Title
		NoPart = s.replace(keyword," ")
	else:
		NoPart = s
	return NoPart

	
def removeGroupKeywordsAndAfter(s):
	processedString = s
	for Part in GroupKeywords:
		processedString = removePartAndAfter(processedString,Part)
	return processedString
	
def removePartAndAfter(s,keyword):
	#don't add spaces if already space in keyword
	if keyword.find(" ") == -1:
		keyword = " " + keyword + " "
	partIndex = s.rfind(keyword)
	if partIndex != -1:
		#remove Part and trailing information from Title
		NoPart = s[:partIndex]
	else:
		NoPart = s
	return NoPart

	
def storyArc_cleanup(storyarc):
	#print "StoryArc before clean up == |" + storyarc + "|"
	#clean up possible StoryArc 
	#remove left over "Part" from books like "Arc Part 1" "Arc Part 2"
	for Part in GroupKeywords:
		storyarc = storyarc.replace(" " + Part, "")
		storyarc = storyarc.replace("(" + Part, "")
	
	#remove whitespace from start and end of string
	storyarc = storyarc.strip()
	
	#remove trailing commas - and ( :
	storyarc = storyarc.rstrip(',-(:')
	
	#remove semi-colon. Used as Story title delimiter
	storyarc = storyarc.strip(';')
	
	#remove whitespace from start and end of string, again
	storyarc = storyarc.strip()
	#print "StoryArc after clean up == |" + storyarc + "|"
	return storyarc
