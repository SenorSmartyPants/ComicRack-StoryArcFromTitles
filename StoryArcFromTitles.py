# StoryArcFromTitles.py
#
# Attempts to parse Titles to find Story Arc Info 
# 
#
# You are free to modify and distribute this file
##########################################################################

import clr, re
import System 

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System.Windows.Forms import *
from System.Drawing import Point, Size

import MethodForm
from MethodForm import MethodForm

import config
from titleparsing import *

#@Name	Get Story Arcs from Titles...
#@Hook	Books
#@Description Get Story Arcs from Titles...
#@Image StoryArcFromTitles.png
#@Key StoryArcFromTitles
def StoryArcFromTitles(books):
	config.LoadSettings()
	#test to make sure there is more than one book
	if len(books) == 0:
		MessageBox.Show("You must select at least 1 book to run this script", "Story Arc From Titles", MessageBoxButtons.OK, MessageBoxIcon.Warning)

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

def SingleStoryArcFromTitles(books):
	titleArray = makeTitleArray(books)
	storyarc = SingleStoryArcFromTitleArray(titleArray, len(books))

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
				ProcessAlternateSeries(book, book.Title, storyarc,result == 2, config.settings["field"], False)
#end SingleStoryArcFromTitles


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
			inv = InvertDictionary(storyarcs)
			updateBooksAlternateSeries(books, inv, result == 2)

#end MultipleStoryArcsFromTitles

