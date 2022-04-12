import clr, re
import System 

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System.Windows.Forms import *
from System.Drawing import Point, Size

from System.IO import FileInfo

#Some important constants
FOLDER = FileInfo(__file__).DirectoryName + "\\"
ICON = FOLDER + "StoryArcFromTitles.ico"
SETTINGSFILE = FOLDER + "settings.dat"

#@Key StoryArcFromTitles
#@Hook ConfigScript
def StoryArcFromTitlesOptions():
    #settings = 
	global settings
	LoadSettings()

	optionform = OptionsForm(settings)

	result = optionform.ShowDialog()

	if result == DialogResult.OK:
		settings["field"] = optionform._cblMethod.Text
		settings["GroupKeywordColon"] = "True" if optionform._chkColon.Checked else "False"
		settings["StripLeadingThe"] = "True" if optionform._chkStripLeadingThe.Checked else "False"
		SaveSettings(settings)

def LoadSettings():
	global settings
    #Define some default settings
	settings = {"field" : "Story Arc", "GroupKeywordColon" : "True", "StripLeadingThe" : "False"}

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
	def __init__(self, settings):
		self.InitializeComponent()
		self._cblMethod.Text = settings["field"]
		self._chkColon.Checked = settings["GroupKeywordColon"] == 'True'
		self._chkStripLeadingThe.Checked = settings["StripLeadingThe"] == 'True'
	
	def InitializeComponent(self):
		self._cblMethod = System.Windows.Forms.ComboBox()
		self._lblDescription = System.Windows.Forms.Label()
		self._lblInstructions = System.Windows.Forms.Label()
		self._btnContinue = System.Windows.Forms.Button()
		self._btnCancel = System.Windows.Forms.Button()
		self._chkColon = System.Windows.Forms.CheckBox()
		self._chkStripLeadingThe = System.Windows.Forms.CheckBox()
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
		# chkColon
		# 
		self._chkColon.AutoCheck = True
		self._chkColon.Location = System.Drawing.Point(12, 60)
		self._chkColon.Name = "chkColon"
		self._chkColon.Size = System.Drawing.Size(300, 21)
		self._chkColon.TabIndex = 1
		self._chkColon.Text = "End Story Arc at colon (:)?"

		# 
		# chkColon
		# 
		self._chkStripLeadingThe.AutoCheck = True
		self._chkStripLeadingThe.Location = System.Drawing.Point(12, 81)
		self._chkStripLeadingThe.Name = "chkColon"
		self._chkStripLeadingThe.Size = System.Drawing.Size(300, 21)
		self._chkStripLeadingThe.TabIndex = 1
		self._chkStripLeadingThe.Text = "Strip leading The from story arc"

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
		self._btnContinue.Location = System.Drawing.Point(156, 101)
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
		self._btnCancel.Location = System.Drawing.Point(237, 101)
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
		self.ClientSize = System.Drawing.Size(336, 135)
		self.Controls.Add(self._btnCancel)
		self.Controls.Add(self._btnContinue)
		self.Controls.Add(self._lblInstructions)
		self.Controls.Add(self._lblDescription)
		self.Controls.Add(self._cblMethod)
		self.Controls.Add(self._chkColon)
		self.Controls.Add(self._chkStripLeadingThe)
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