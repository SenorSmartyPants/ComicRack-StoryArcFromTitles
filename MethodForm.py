import clr
import System

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
#clr.AddReference("PresentationFramework")
#clr.AddReference("PresentationCore")

#from System.Windows.Interop import WindowInteropHelper

import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

from System.IO import FileInfo

#Some important constants
FOLDER = FileInfo(__file__).DirectoryName + "\\"
ICON = FOLDER + "StoryArcFromTitles.ico"

class MethodForm(Form):
	def __init__(self):
		self.InitializeComponent()
	
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
			["Default - Multiple Story Arcs - Truncate \"part\" and after",
			"Alternate - Multiple Story Arcs - Remove only \"part\"",
			"Single - Single Story Arc - Strict matching"]))
		self._cblMethod.Location = System.Drawing.Point(12, 72)
		self._cblMethod.Name = "cblMethod"
		self._cblMethod.Size = System.Drawing.Size(300, 21)
		self._cblMethod.TabIndex = 0
		# 
		# lblDescription
		# 
		self._lblDescription.Location = System.Drawing.Point(12, 9)
		self._lblDescription.Name = "lblDescription"
		self._lblDescription.Size = System.Drawing.Size(325, 18)
		self._lblDescription.TabIndex = 1
		self._lblDescription.Text = "The selected books' titles will be scanned for story arcs."
		# 
		# lblInstructions
		# 
		self._lblInstructions.Location = System.Drawing.Point(12, 49)
		self._lblInstructions.Name = "lblInstructions"
		self._lblInstructions.Size = System.Drawing.Size(325, 23)
		self._lblInstructions.TabIndex = 2
		self._lblInstructions.Text = "Choose method to use to detect story arcs, or leave as default:"
		# 
		# btnContinue
		# 
		self._btnContinue.DialogResult = System.Windows.Forms.DialogResult.OK
		self._btnContinue.Location = System.Drawing.Point(156, 110)
		self._btnContinue.Name = "btnContinue"
		self._btnContinue.Size = System.Drawing.Size(75, 23)
		self._btnContinue.TabIndex = 0
		self._btnContinue.Text = "Continue"
		self._btnContinue.UseVisualStyleBackColor = True
		self._btnContinue.Click += self.BtnContinueClick
		# 
		# btnCancel
		# 
		self._btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
		self._btnCancel.Location = System.Drawing.Point(237, 110)
		self._btnCancel.Name = "btnCancel"
		self._btnCancel.Size = System.Drawing.Size(75, 23)
		self._btnCancel.TabIndex = 4
		self._btnCancel.Text = "Cancel"
		self._btnCancel.UseVisualStyleBackColor = True
		self._btnCancel.Click += self.BtnCancelClick
		# 
		# MethodForm
		# 
		self.AcceptButton = self._btnContinue
		self.CancelButton = self._btnCancel
		self.ClientSize = System.Drawing.Size(336, 144)
		self.Controls.Add(self._btnCancel)
		self.Controls.Add(self._btnContinue)
		self.Controls.Add(self._lblInstructions)
		self.Controls.Add(self._lblDescription)
		self.Controls.Add(self._cblMethod)
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Name = "MethodForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		self.Text = "Story Arc from Titles"
		self.Icon = System.Drawing.Icon(ICON)
		self.Load += self.MainFormLoad
		self.ResumeLayout(False)

	def MainFormLoad(self, sender, e):
		self._cblMethod.SelectedIndex = 0

	def BtnContinueClick(self, sender, e):
		self.Close()

	def BtnCancelClick(self, sender, e):
		self.Close()