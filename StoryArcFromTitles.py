# StoryArcFromTitles.py
#
# Attempts to parse Titles to find Story Arc Info 
# 
#
# You are free to modify and distribute this file
##########################################################################

import clr, re
import System 
from System.IO import FileInfo

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System.Windows.Forms import *
from System.Drawing import Point, Size

import MethodForm
from MethodForm import MethodForm

from titleparsing import *

#@Name	Get Story Arcs from Titles...
#@Hook	Books
#@Description Get Story Arcs from Titles...
#@Image StoryArcFromTitles.png
#@Key StoryArcFromTitles
def StoryArcFromTitles(books):
	global settings
	settings = LoadSettings()
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

def SingleStoryArcFromTitles(books):
	global settings
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
				ProcessAlternateSeries(book,storyarc,result == 2, settings["field"])
#end SingleStoryArcFromTitles


def MultipleStoryArcsFromTitles(books,method_selected):
	global settings
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
				arcsFound = 0
				splitTitle = book.Title.split(";")
				for	title in splitTitle:
					if inv.has_key(title):
						arcsFound += 1
						storyarc = inv[title]
						ProcessAlternateSeries(book,storyarc,result == 2, settings["field"], arcsFound > 1)

#end MultipleStoryArcsFromTitles

#Some important constants
FOLDER = FileInfo(__file__).DirectoryName + "\\"
ICON = FOLDER + "StoryArcFromTitles.ico"
SETTINGSFILE = FOLDER + "settings.dat"

#@Key StoryArcFromTitles
#@Hook ConfigScript
def StoryArcFromTitlesOptions():
    
    settings = LoadSettings()

    optionform = OptionsForm(settings["field"])

    result = optionform.ShowDialog()

    if result == DialogResult.OK:
        settings["field"] = optionform._cblMethod.Text
        SaveSettings(settings)

def LoadSettings():
    #Define some default settings
    settings = {"field" : "Story Arc"}

    #The settings file should be formated with each line as SettingName:Value. eg Prefix:Scanner:

    try:
        with open(SETTINGSFILE, 'r') as settingsfile:
            for line in settingsfile:
                match = re.match("(?P<setting>.*?):(?P<value>.*)", line)
                settings[match.group("setting")] = match.group("value")

    except Exception, ex:
        print "Something has gone wrong loading the settings file. The error was: " + str(ex)
    
    return settings		

def SaveSettings(settings):
    
    with open(SETTINGSFILE, 'w') as settingsfile:
        for setting in settings:
            settingsfile.write(setting + ":" + settings[setting] + "\n")

class OptionsForm(Form):
	def __init__(self, field):
		self.InitializeComponent()
		self._cblMethod.Text = field
	
	def InitializeComponent(self):
		self._cblMethod = System.Windows.Forms.ComboBox()
		self._lblDescription = System.Windows.Forms.Label()
		self._lblInstructions = System.Windows.Forms.Label()
		self._btnContinue = System.Windows.Forms.Button()
		self._btnCancel = System.Windows.Forms.Button()
		self.SuspendLayout()
		# 
		# cblMethod
		# 
		self._cblMethod.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._cblMethod.FormattingEnabled = True
		self._cblMethod.Items.AddRange(System.Array[System.Object](
			["Story Arc",
			"Alternate Series"]))
		self._cblMethod.Location = System.Drawing.Point(12, 32)
		self._cblMethod.Name = "cblMethod"
		self._cblMethod.Size = System.Drawing.Size(300, 21)
		self._cblMethod.TabIndex = 0
		# 
		# lblInstructions
		# 
		self._lblInstructions.Location = System.Drawing.Point(12, 9)
		self._lblInstructions.Name = "lblInstructions"
		self._lblInstructions.Size = System.Drawing.Size(325, 23)
		self._lblInstructions.TabIndex = 2
		self._lblInstructions.Text = "Choose in which field to store story arc found in title:"
		# 
		# btnContinue
		# 
		self._btnContinue.DialogResult = System.Windows.Forms.DialogResult.OK
		self._btnContinue.Location = System.Drawing.Point(156, 70)
		self._btnContinue.Name = "btnContinue"
		self._btnContinue.Size = System.Drawing.Size(75, 23)
		self._btnContinue.TabIndex = 0
		self._btnContinue.Text = "Ok"
		self._btnContinue.UseVisualStyleBackColor = True
		self._btnContinue.Click += self.BtnContinueClick
		# 
		# btnCancel
		# 
		self._btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
		self._btnCancel.Location = System.Drawing.Point(237, 70)
		self._btnCancel.Name = "btnCancel"
		self._btnCancel.Size = System.Drawing.Size(75, 23)
		self._btnCancel.TabIndex = 4
		self._btnCancel.Text = "Cancel"
		self._btnCancel.UseVisualStyleBackColor = True
		self._btnCancel.Click += self.BtnCancelClick
		# 
		# OptionsForm
		# 
		self.AcceptButton = self._btnContinue
		self.CancelButton = self._btnCancel
		self.ClientSize = System.Drawing.Size(336, 104)
		self.Controls.Add(self._btnCancel)
		self.Controls.Add(self._btnContinue)
		self.Controls.Add(self._lblInstructions)
		self.Controls.Add(self._lblDescription)
		self.Controls.Add(self._cblMethod)
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Name = "OptionsForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		self.Text = "Story Arc from Titles Options"
		self.Icon = System.Drawing.Icon(ICON)
		self.ResumeLayout(False)

	def BtnContinueClick(self, sender, e):
		self.Close()

	def BtnCancelClick(self, sender, e):
		self.Close()