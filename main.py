import os
os.environ['KIVY_VIDEO'] = 'ffpyplayer'
os.environ['KIVY_IMAGE'] = 'pil'
os.environ['KIVY_AUDIO'] = 'ffpyplayer'

import sys
import time
import datetime
from dateutil.relativedelta import relativedelta
import random
import cv2
import threading
import multiprocessing
from functools import partial
import asynckivy as ak
from asynckivy.process_and_thread import thread
from progressspinner import ProgressSpinner
import mysql.connector
import firebase_admin
from firebase_admin import credentials,auth
import pyrebase

cred = credentials.Certificate("pulse_firebase.json")


from kivy.metrics import dp
from kivy.app import App 
from kivy.core.window import Window 
from kivy.core.audio import SoundLoader
from kivy.animation import Animation 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock 
from kivy.factory import Factory
from kivy.uix.screenmanager import *
from kivy.uix.effectwidget import EffectWidget,PixelateEffect, HorizontalBlurEffect
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.uix.recycleview import RecycleView 
from kivy.uix.recycleboxlayout import RecycleBoxLayout 
from kivy.uix.modalview import ModalView
from kivy.uix.bubble import Bubble
from kivy.effects.dampedscroll import DampedScrollEffect
from kivy.core.clipboard import Clipboard
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase


from kivymd.uix.behaviors.touch_behavior import TouchBehavior
from kivymd.uix.behaviors.backgroundcolorbehavior import (
    BackgroundColorBehavior,
    SpecificBackgroundColorBehavior,
)
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.behaviors.ripplebehavior import CircularRippleBehavior,RectangularRippleBehavior
from kivymd.uix.behaviors.magic_behavior import MagicBehavior 
from kivymd.uix.behaviors.elevation import CircularElevationBehavior,RectangularElevationBehavior
from kivymd.theming import ThemableBehavior
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField, MDTextFieldRound,MDTextFieldRect
from kivymd.uix.button import *
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel, MDIcon 
from kivymd.uix.card import MDSeparator, FullSeparator
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.spinner import MDSpinner
from kivymd.stiffscroll import StiffScrollEffect
from kivymd.uix.card import MDCard, MDCardPost
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.imagelist import SmartTile
from kivymd.uix.slider import MDSlider
from kivymd.uix.dialog import MDDialog
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.tab import MDTabs,MDTabsBase
from kivymd.utils.fitimage import FitImage
from kivymd.utils.roundfitimage import RoundFitImage 
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.refreshlayout import RefreshSpinner, MDScrollViewRefreshLayout

def toast(text):
    from kivymd.toast.kivytoast import toast
    toast(text)

acceptaple_char = "abcdefghijklmnopqrstuvwxyz1234567890_.' "


def create_video_thumbnail(filename):
	cap = cv2.VideoCapture(filename)
	video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
	frame = None
	if cap.isOpened() and video_length > 0:
		fps = cap.get(cv2.CAP_PROP_FPS)
		duration = (video_length/fps)
		seek = (3/duration)*video_length
		try:
			cap.set(1,seek)
		except:
			pass
		success, image = cap.read()
		while success:
			frame =image
			break
	height, width, channels = frame.shape
	basename = os.path.splitext(filename)[0]
	b_name = basename.replace('/','_')
	name = b_name.replace('\\','_')
	if os.path.exists('thumbnail'):
		pass
	else:
		os.makedirs('thumbnail')
	'''
	res, thumb_buf = cv2.imencode('.png', frame)
	bt = thumb_buf.tostring()'''
	if os.path.exists('thumbnail/%s.png' % (name)):
		os.remove('thumbnail/%s.png' % (name))
	try:
		cv2.imwrite('thumbnail/%s.png' % (name), frame)
		return ('thumbnail/%s.png' % (name))
	except:
		# try to restore deleted thumbnail
		return ('assets/purple.jpg')


def post_timestamp(instance_time):
	posted_time = instance_time.strftime("%Y-%m-%d %H:%M:%S")
	post_time = datetime.datetime.strptime(str(posted_time),'%Y-%m-%d %H:%M:%S')
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	post_now = datetime.datetime.strptime(str(now),'%Y-%m-%d %H:%M:%S')
	diff  = relativedelta(post_now,post_time)
	months = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
	#print ("The difference is %d year %d month %d days %d hours %d minutes and %d seconds." % (diff.years, diff.months, diff.days, diff.hours, diff.minutes,diff.seconds))
	diff_text = ("%d minutes and %d seconds." % (diff.minutes,diff.seconds))
	if diff.years>0:
		posted_year = str(instance_time.strftime("%Y"))
		posted_month = str(instance_time.strftime("%m"))
		posted_date = str(instance_time.strftime("%d"))
		diff_text = (months[posted_month]+' '+posted_date+', '+posted_year)
	elif diff.months>0:
		posted_month = str(instance_time.strftime("%m"))
		posted_date = str(instance_time.strftime("%d"))
		diff_text = (months[posted_month]+' '+posted_date)
	elif diff.days>0:
		if diff.days==1:
			today = datetime.datetime.now().strftime("%d")
			post_day = instance_time.strftime("%d")
			if int(today)-int(post_day) == 1:
				diff_text = "Yesterday"
			else:
				diff_text = "%d days ago" %(int(today)-int(post_day),)
		else:
			diff_text = "%d days ago" %(diff.days,)
	elif diff.hours>0:
		if diff.hours == 1:
			diff_text = "%d hour ago" %(diff.hours,)
		else:
			diff_text = "%d hours ago" %(diff.hours,)
	elif diff.minutes>0:
		if diff.minutes == 1:
			diff_text = "%d minute ago" %(diff.minutes,)
		else:
			diff_text = "%d minutes ago" %(diff.minutes,)
	elif diff.seconds>0:
		if diff.seconds == 1:
			diff_text = "%d second ago" %(diff.seconds,)
		else:
			diff_text = "%d seconds ago" %(diff.seconds,)
	else:
		diff_text = "Now"
	return diff_text



LabelBase.register(name = "champ", 
    fn_regular = "fonts/cac_champagne.ttf" )



kv_file = Builder.load_string(
"""
#:import sm kivy.uix.screenmanager
<FullScreen>
	canvas:
		Color:
			rgba : [1,1,1,.1]
		RoundedRectangle:
			id: background
			size: self.size
            pos: self.pos
            radius: app.radii

<LoginScreen>
	orientation: "vertical"
	size_hint : (.8,.7)
	pos_hint : {'center_x': .5,'center_y': .3}
	MDSeparator:
	ScreenManager:
		id : log_sign_screens
		Screen:
			name: 'login_screen'
			BoxLayout:
				id: log_layout
				orientation: "vertical"
				pos_hint: {'center_x':.5}
				padding: 5
				MDTextField:
					id:loguser
				    hint_text: "Username"
				    helper_text_mode: "on_error"
				    required: True
				    on_text_validate: logpassword.focus=True
				Widget:
					size_hint_y:None
					height:app.window.height/35
				RelativeLayout:
					size_hint: 1,None
					height: logpassword.height
					MDTextField:
						id:logpassword
						hint_text: "Password"
						password: True
						password_mask: "*"
						helper_text_mode: "on_error"
					    required: True
					    on_text_validate: app.login(loguser.text,self.text, notification_layout,login_b) if loguser.text != '' and logpassword.text != '' else app.passs()
					MDIconButton:
						pos_hint: {'right': 1, 'top':1}
						icon: 'eye-off' if logpassword.password == True else 'eye'
						on_press:
							logpassword.focus=True
							logpassword.password = False if logpassword.password == True else True
						on_release: 
							logpassword.focus=True
				MDTextButton:
					size_hint_y:None
					height:dp(18)
					text: 'Forgot Password?'
					pos_hint: {'right': 1}
				Widget:
					size_hint_y:None
					height:app.window.height/20
				RelativeLayout:
					pos_hint: {'center_x': .5}
					size_hint:None,None
					size: login_b.size
					MDFillRoundFlatButton:
						id: login_b
						text: 'Login'
						pos_hint: {'center_x': .5}
						theme_text_color:'Custom'
						text_color:[1,1,1,1]
						icon: 'login'
						disabled:False if loguser.text != '' and logpassword.text != '' else True
						on_press:
							app.login(loguser.text,logpassword.text, notification_layout,self)
						canvas.after:
							Color:
								rgba:[1,1,1,.5] if self.disabled == True else [0,0,0,0]
							RoundedRectangle:
								size:self.size
								pos:self.pos
								radius:[dp(18),]
				BoxLayout:
					id: notification_layout
					size_hint: 1,.25
					padding: dp(5)
				BoxLayout:
					orientation: 'vertical'
					size_hint_y:.2
					spacing: 10
					pos_hint: {'center_y': .1}
					BoxLayout:
				    	size_hint_x:.75
				    	pos_hint: {'center_x': .5}
				    	spacing: dp(5)
					    MDTextButton:
					    	text:"Don't have an account?"
					    	font_size: dp(15)
					    	custom_color: [0,0,0,1]
							pos_hint: {'center_y': .5}
					    MDTextButton:
					    	text: "Signup"
					    	custom_color: [0,0,1,1]
					    	font_size: dp(15)
					    	pos_hint: {'center_y': .5}
					    	on_press:
					    		root.ids.log_sign_screens.transition.direction = 'left'
					    		root.ids.log_sign_screens.current = "signup_screen"
					MDSeparator:
					MDTextButton:
						text: "Explore without Account"
						font_size: dp(15)
						custom_color: [0,0,.5,1]
						pos_hint: {'center_x': .5, 'center_y': .5}
				Widget:
					size_hint_y:.1



		Screen:
			name: 'signup_screen'
			BoxLayout:
				orientation: "vertical"
				pos_hint: {'center_x':.5}
				spacing: dp(10)
				padding: 5

				MDTextField:
					id: user
				    hint_text: "Username"
				    helper_text_mode: "on_error"
				    required: True
				    on_text_validate: email.focus=True
				MDTextField:
					id: email
				    hint_text: "Email"
				    required: True
				    on_text_validate: phone.focus=True
				MDTextField:
					id: phone
				    hint_text: "Phone Number"
				    on_text_validate: password.focus=True
				RelativeLayout:
					size_hint: 1,None
					height: password.height
					MDTextField:
						id: password
						hint_text: "Password"
						password: True
						password_mask: "*"
						helper_text_mode: "on_error"
					    required: True
					    on_text_validate: app.signup(user.text, email.text, phone.text, self.text,s_notification_layout,signup_b) if user.text != '' and password.text != '' and email.text != '' else app.passs()
					MDIconButton:
						pos_hint: {'right': 1, 'top':1}
						icon: 'eye-off' if password.password == True else 'eye'
						on_press:
							password.focus=True
							password.password = False if password.password == True else True
						on_release:
							password.focus=True
				RelativeLayout:
					pos_hint: {'center_x': .5}
					size_hint:None,None
					size:signup_b.size
					MDFillRoundFlatButton:
						id:signup_b
						text: 'Signup'
						pos_hint: {'center_x': .5}
						disabled:False if user.text != '' and password.text != '' and email.text != '' else True
						on_press: app.signup(user.text, email.text, phone.text, password.text,s_notification_layout,self) if user.text != '' and password.text != '' and email.text != '' else app.passs()
						canvas.after:
							Color:
								rgba:[1,1,1,.5] if self.disabled == True else [0,0,0,0]
							RoundedRectangle:
								size:self.size
								pos:self.pos
								radius:[dp(18),]
				BoxLayout:
					id: s_notification_layout
					size_hint: 1,.25
					padding: dp(5)
				BoxLayout:
					orientation: 'vertical'
					spacing: 10
					size_hint_y: .2
					pos_hint: {'center_y': .1}
					BoxLayout:
				    	size_hint_x:.8
				    	pos_hint: {'center_x': .5}
				    	spacing: dp(5)
					    MDTextButton:
					    	text:"Already have an account?"
					    	font_size: dp(15)
					    	custom_color: [0,0,0,1]
							pos_hint: {'center_y': .5}
					    MDTextButton:
					    	text: "Login"
					    	custom_color: [0,0,1,1]
					    	font_size: dp(15)
					    	pos_hint: {'center_x': .5,'center_y': .5}
					    	on_press:
					    		root.ids.log_sign_screens.transition.direction = 'right'
					    		root.ids.log_sign_screens.current = "login_screen"
					MDSeparator:
				Widget:
					size_hint_y:.1
<InterestScreen>
	orientation: 'vertical'
	size_hint: 1,1
	padding: dp(10)
	BoxLayout:
		orientation: 'vertical'
		size_hint: 1,.3
		MDLabel:
			text: 'What are your Interests?'
			size_hint_x: 1
			pos_hint: {'center_x': .5}
			font_size: dp(20)
			bold: True
			halign: 'center'
		MDLabel:
			text: 'Please select your fields of interests. Choose content that you would like to be displayed for you. The more you got, the greater the fun!'
			size_hint_x: .8
			halign: 'center'
			font_size: dp(15)
			pos_hint: {'center_x': .5}
	ScrollView:
		size_hint: 1, 1
		effect_cls: 'ScrollEffect'
		GridLayout:
			id: interests_scroll
			size_hint: 1,None
			cols:1
			padding: dp(10)
	        spacing: dp(15)
			height: self.minimum_height
	BoxLayout:
		size_hint: 1,.1
		padding: dp(10)
		pos_hint: {'bottom': 1}
		MDLabel:
			id: interest_count
			text: '0'
			pos_hint: {"center_y": 0.5}
		Widget:
		MDTextButton:
			text: 'Done'
			pos_hint: {"center_y": 0.5}
			on_press: app.save_interests()
<InterestCard>
	orientation:'vertical'
	size_hint: 1,None
	height: category.height+subcategory.height
	InterestLayout:
		height: dp(32.5)
		id: category
		on_press: 
			app.interest_subcategory(interest_check,root.idd, 'pic',subcategory,root.sub) if root.pres == 'sub_interests' else app.select_interest(interest_check,root.idd)
		canvas.before:
			Color:
				rgba: [1,1,1,.3]
			RoundedRectangle:
				pos: self.pos
				source: 'assets/purple.jpg'
				size: self.size
				radius:[12]
		canvas.after:
			Color:
				rgba: [1,0,1,.5]
			Line:
				width: 1
				rounded_rectangle: (self.x, self.y, self.width, self.height,\
	                12,12, 12,12,\
	                self.height)
		MDIconButton:
			icon:root.source
			pos_hint: {"center_y": 0.5}
		MDLabel:
			id: interest_category
			text: ''
			pos_hint: {"center_x": 0.5}
			halign: 'left'
			size_hint_x:1
			shorten: True
			shorten_from: 'right'
		MDIconButton:
			id: interest_check
			icon: 'checkbox-blank-circle-outline'
			theme_text_color: 'Custom'
			text_color: [0,0,0,1]
			pos_hint: {"center_y": 0.5}
			on_press: app.interest_subcategory(self, root.idd, 'check', subcategory,root.sub) if root.pres == 'sub_interests' else app.select_interest(self,root.idd)
	GridLayout:
		cols: 1
		id: subcategory
		occupied: 'No'
		size_hint: .8, None
		height: dp(0)
		padding: dp(5)
		spacing: dp(5)
		pos_hint: {'right':1}
<InterestSubcategory>
	height: dp(32.5)
	id: category
	on_press: 
		app.select_interest(interest_check,root.idd)
	canvas.before:
		Color:
			rgba: [1,1,1,.3]
		RoundedRectangle:
			pos: self.pos
			source: 'assets/purple.jpg'
			size: self.size
			radius:[12]
	canvas.after:
		Color:
			rgba: [1,0,1,.5]
		Line:
			width: 1
			rounded_rectangle: (self.x, self.y, self.width, self.height,\
	            12,12, 12,12,\
	            self.height)
	MDIconButton:
		icon:root.source
		pos_hint: {"center_y": 0.5}
	MDLabel:
		id: subinterests_title
		text: ''
		pos_hint: {"center_x": 0.5}
		halign: 'left'
		size_hint_x:1
		shorten: True
		shorten_from: 'right'
	MDIconButton:
		id: interest_check
		icon: 'checkbox-blank-circle-outline'
		theme_text_color: 'Custom'
		text_color: [0,0,0,1]
		pos_hint: {"center_y": 0.5}
		on_press:app.select_interest(self,root.idd)
<RootManager>
	Screen:
		name: 'basic_root'
		id: basic_root
		RootScreen:
			id: rootscreen
			transition: sm.NoTransition(duration=0)
			size_hint: 1,.9
			pos_hint: {'top':1}
			canvas:
				Color:
					rgba: [1,1,1,1]
				Rectangle:
					size:self.size
					pos:self.pos
		MDCard:
			id:bottom_navigation
			orientation: 'horizontal'
			size_hint: 1,.1
			pos_hint: {'bottom':1}
			canvas:
				Color:
					rgba: [1,1,1,.025]
				Rectangle:
					source: 'assets/bottomnav.png'
					size:self.size
					pos:self.pos
			ButtonBoxLayoutPlain:
				on_press: app.change_screen('home_screen')
				MDIcon:
					id: home
					icon: 'home'
					theme_text_color: 'Custom'
					font_size: (bottom_navigation.height)*0.45 if rootscreen.current == 'home_screen' else (bottom_navigation.height)*0.4
					text_color: [.5,0,1,1] if rootscreen.current == 'home_screen' else [0,0,0,.5]
					valign: 'middle'
        			halign: 'center'
				
			ButtonBoxLayoutPlain:
				on_press:app.change_screen('my_galaxy')
				MDIcon:
					id: galaxy
					icon: 'earth'
					theme_text_color: 'Custom'
					size_hint: 1,1
					font_size: (bottom_navigation.height)*0.45 if rootscreen.current == 'my_galaxy' else (bottom_navigation.height)*0.4
					text_color: [.5,0,1,1] if rootscreen.current == 'my_galaxy' else [0,0,0,.5]
					valign: 'middle'
        			halign: 'center'
        	ButtonBoxLayoutPlain:
        		on_press:app.posting()
				MDIcon:
					icon: 'plus-circle'
					theme_text_color: 'Custom'
					size_hint: 1,1
					font_size: (bottom_navigation.height)*0.95
					text_color: [1,.75,.25,1]
					valign: 'middle'
        			halign: 'center'
				
			ButtonBoxLayoutPlain:
				on_press:app.change_screen('challenges_screen')
				MDIcon:
					id: challenges
					icon: 'certificate'
					theme_text_color: 'Custom'
					size_hint: 1,1
					font_size: (bottom_navigation.height)*0.45 if rootscreen.current == 'challenges_screen' else (bottom_navigation.height)*0.4
					text_color: [.5,0,1,1] if rootscreen.current == 'challenges_screen' else [0,0,0,.5]
					valign: 'middle'
        			halign: 'center'
				
			
			ButtonBoxLayoutPlain:
				on_press:app.change_screen('my_profile')
				padding:app.window.height*0.025
				RoundImage:
					id: myprofile
					elevation: 1 if rootscreen.current == 'my_profile' else 0
					size_hint: None,None
					height: (bottom_navigation.height)*0.45 if rootscreen.current == 'my_profile' else (bottom_navigation.height)*0.4
					width: self.height
					pos_hint: {'center_x':.5,'center_x':.5}
				
<MySpinner>
	active: True
	color: [.5,0,1,.75]
	size_hint: .15,.15
	pos_hint: {"center_x": 0.5, "center_y": .8}
<MyRecycleView>
	key_viewclass: 'viewclass'
    key_size: 'height'
<MyRecycleBoxLayout>
    padding: dp(0)
    spacing: dp(10)
    id: recycle_layout
    default_size: None, None
    default_size_hint:1, None
    size_hint_y: None
    height: self.minimum_height
    orientation: 'vertical'
<ImageLayoutMultiple>
	id:post_card
    orientation: 'vertical'
    spacing: dp(1)
    padding: dp(0)
    post_image: ''
    info: 
    height: root.virtual_height + root.info +dp(10)
    size_hint:(None,None)
    width: app.window.width
    previous_dialog: None
    pos_hint:{'center_x': .5}
    username: ""
    category: ""
    caption: ""	
    likes: ""
    comments: ""
    duration: ""
    comment_1: ""
    comment_2: ""
    BoxLayout:
    	orientation: "horizontal"
    	size_hint:1, None
    	height: dp(55)
    	padding:dp(1)
    	BoxLayout:
    		orientation: 'vertical'
    		size_hint: None,1
    		width: (app.window.width*0.5)-((dp(50))/2)
	    	MyTextButton:
	        	text: root.username
	        	theme_text_color: 'Custom'
			    text_color:[.1,0,.2,1]
			    halign: 'center'
	        	font_size: dp(18)
	        	shorten: True
	        	shorten_from: 'right'
	        	on_press: app.profile([root.post_info[1],root.post_info[6],root.post_info[7]],root)
	        MDLabel:
	        	id: emotion
	        	text: root.emotion
	        	font_size: dp(15)
	        	halign: 'center'
	        	theme_text_color: 'Custom'
			    text_color:[0,0,0,.75]
	        	shorten: True
	        	shorten_from: 'right'
        RoundImageTouch:
	        source: root.profilepic
	        on_press: app.profile([root.post_info[1],root.post_info[6],root.post_info[7]],root)
	        size_hint: None,None
	        pos_hint: {'center_y':.5}
	        size: dp(50),dp(50)
	    Widget:
    	MDIconButton:
    		icon: 'dots-vertical'
    		pos_hint: {'center_y':.5}
    		on_press:
    			app.post_options(root.post_info,root)
    			print(root.height)

    RelativeLayout:
    	id: relative_layout
    	size_hint: 1, None
    	height: root.post_height
    	texture: image.texture
    	width: root.width
    	padding:dp(0)
    	Carousel:
    		id: carousel
    		loop: True
    		RelativeLayout:
    			size_hint:1,1
    			EffectWidget:
		    		size_hint: 1, 1
			    	id: image_blur
					BlurVideoBg:
						id: blur
						size_hint:1,1
						canvas.after:
							Color:
								rgba: [1,1,1,1]
							Rectangle:
								texture: relative_layout.texture
								pos: self.pos
								size: self.size #image_ratio
			    ImageTouch:
			        id: image
			        source: root.source
			        allow_stretch: True
			        size_hint: 1, None
			        keep_ratio: True
			        size: post_card.width, post_card.width/self.image_ratio
			        pos_hint: {'center_y': .5,'center_x': .5}

	    BoxLayout:
	    	padding: 0
	    	size_hint_y: None
	    	height: self.minimum_height
	    	width:image.width
	    	pos_hint: {'bottom': 1,'center_x': .5}
	    	Widget:
	    		size_hint_x: None
	    		width: dp(10)
			ImgHeartIcon:
				id: like_icon
				on_release:
					app.like_post(root.post_info,root.likecomment)
			Widget:
			BoxLayout:
				size_hint: None,None
				height: dp(30)
				width: dp(50)
				pos_hint: {'center_y':.5}
				canvas:
		    		Color:
		    			rgba: [1,.85,.5,.4]
		    		RoundedRectangle:
		    			size: self.size
		    			pos: self.pos
		    			radius:[10]
				MDLabel:
			    	text: str(carousel.index+1)+'/'+str(len(carousel.slides))
			    	font_size: dp(15)
			    	bold: True
			    	halign: 'center'
			    	max_lines:1
			    	size_hint: None,None
			    	height: dp(20)
			    	width: self.parent.width
			    	pos_hint:{'center_y':.5, 'center_x':.5}
		    	
		    Widget:
		    	size_hint_x: None
	    		width: dp(10)
    
    BoxLayout:
    	orientation: "vertical"
    	size_hint:1,None
    	spacing: dp(0)
    	padding: dp(5)
		id: post_info
		height: root.info +dp(10)
		BoxLayout:
			id:multiple_index
			size_hint:None,None
			width:self.minimum_width
			pos_hint:{'center_x':.5}
			height:dp(10)
			spacing:dp(5)
		BoxLayout:
			id: caption_lay
			size_hint:1,None
			height:self.minimum_height
	    	DynamicLabel:
	    		id: caption
	    		size_hint_y: None
	    		text_size: None, None
	    		text: 'Caption '
	    		shorten: False
	    		shorten_from:'right'
	    	MDTextButton:
	    		id: caption_button
	    		text:'More' if caption.shorten == True else 'Less'
	    		size_hint:None,None
	    		size: dp(40),dp(20)
	    		custom_color: [.1,.1,.1,.75]
	    		pos_hint:{'right':1,'bottom':1}
	    		on_press:
	    			root.height = root.height+(caption.virtual_height-caption.short_height) if caption.shorten == True else root.height-(caption.virtual_height-caption.short_height)
	    			app.adjust_scroll([root.scroll_layout,(caption.virtual_height-caption.short_height)]) if caption.shorten == True else app.adjust_scroll([root.scroll_layout,(caption.short_height-caption.virtual_height)])
	    			post_info.height = post_info.height+(caption.virtual_height-caption.short_height) if caption.shorten == True else post_info.height-(caption.virtual_height-caption.short_height)
	    			caption.height = caption.virtual_height if caption.shorten == True else caption.short_height
	    			caption.shorten = False if caption.shorten == True else True
<ImageLayout>
	id:post_card
    orientation: 'vertical'
    spacing: dp(1)
    padding: dp(0)
    post_image: ''
    info: 
    height: root.virtual_height + root.info
    size_hint:(None,None)
    width: app.window.width
    previous_dialog: None
    pos_hint:{'center_x': .5}
    username: ""
    category: ""
    caption: ""	
    likes: ""
    comments: ""
    duration: ""
    comment_1: ""
    comment_2: ""
    BoxLayout:
    	orientation: "horizontal"
    	size_hint:1, None
    	height: dp(55)
    	padding:dp(1)
    	BoxLayout:
    		orientation: 'vertical'
    		size_hint: None,1
    		width: (app.window.width*0.5)-((dp(50))/2)
	    	MyTextButton:
	        	text: root.username
	        	theme_text_color: 'Custom'
	        	halign: 'center'
			    text_color:[.1,0,.2,1]
	        	font_size: dp(18)
	        	shorten: True
	        	shorten_from: 'right'
	        	on_press: app.profile([root.post_info[1],root.post_info[6],root.post_info[7]],root)
	        MDLabel:
	        	id: emotion
	        	text: root.emotion
	        	font_size: dp(15)
	        	halign: 'center'
	        	theme_text_color: 'Custom'
			    text_color:[0,0,0,.75]
	        	shorten: True
	        	shorten_from: 'right'
        RoundImageTouch:
	        source: root.profilepic
	        on_press: app.profile([root.post_info[1],root.post_info[6],root.post_info[7]],root)
	        size_hint: None,None
	        pos_hint: {'center_y':.5}
	        size: dp(50),dp(50)
	    Widget:
    	MDIconButton:
    		icon: 'dots-vertical'
    		pos_hint: {'center_y':.5}
    		on_press:
    			app.post_options(root.post_info,root)
    			print(root.height)

    RelativeLayout:
    	size_hint: 1, None
    	height: root.post_height
    	width: root.width
    	id: relative_layout
    	texture: image.texture
    	padding:dp(0)
    	Carousel:
    		size_hint: 1, 1
	    	EffectWidget:
	    		size_hint: 1, 1
		    	id: image_blur
				BlurVideoBg:
					id: blur
					size_hint:1,1
					canvas.after:
						Color:
							rgba: [1,1,1,1]
						Rectangle:
							texture: relative_layout.texture
							pos: self.pos
							size: self.size #image_ratio
					
		ImageTouch:
		    id: image
		    source: root.source
	        allow_stretch: True
	        size_hint: 1, None
	        keep_ratio: True
	        size: post_card.width, post_card.width/self.image_ratio
	        pos_hint: {'center_x': .5,'center_y': .5}
	    BoxLayout:
	    	padding: 0
	    	size_hint_y: None
	    	height: self.minimum_height
	    	width:image.width
	    	pos_hint: {'bottom': 1,'center_x': .5}
	    	Widget:
	    		size_hint_x: None
	    		width: dp(10)
			ImgHeartIcon:
				id: like_icon
				on_release:
					app.like_post(root.post_info,root.likecomment)
			
    BoxLayout:
    	orientation: "vertical"
    	size_hint:1,None
    	spacing: dp(0)
    	padding: dp(5)
		id: post_info
		height: root.info
    	BoxLayout:
			size_hint:1,None
			height:self.minimum_height
			id: caption_lay
	    	DynamicLabel:
	    		id: caption
	    		size_hint_y: None
	    		text_size: None, None
	    		text: 'Caption '
	    		shorten: False
	    		shorten_from:'right'
	    	MDTextButton:
	    		id: caption_button
	    		text:'More' if caption.shorten == True else 'Less'
	    		size_hint:None,None
	    		size: dp(40),dp(20)
	    		custom_color: [.1,.1,.1,.75]
	    		pos_hint:{'right':1,'bottom':1}
	    		on_press:
	    			root.height = root.height+(caption.virtual_height-caption.short_height) if caption.shorten == True else root.height-(caption.virtual_height-caption.short_height)
	    			app.adjust_scroll([root.scroll_layout,(caption.virtual_height-caption.short_height)]) if caption.shorten == True else app.adjust_scroll([root.scroll_layout,(caption.short_height-caption.virtual_height)])
	    			post_info.height = post_info.height+(caption.virtual_height-caption.short_height) if caption.shorten == True else post_info.height-(caption.virtual_height-caption.short_height)
	    			caption.height = caption.virtual_height if caption.shorten == True else caption.short_height
	    			caption.shorten = False if caption.shorten == True else True

<AudioLayout>
	id: audio_card
	orientation: 'vertical'
    spacing: dp(1)
    padding: dp(0)
    height: root.info + dp(50)+dp(4)+audio_info_lay.height
	size_hint:(None,None)
	width: app.window.width
	pos_hint:{'center_x': .5}
    MDCard:
    	orientation:'vertical'
		size_hint: 1,None
		height: self.minimum_height
    	padding:(5)
		BoxLayout:
			id: audio_info_lay
			size_hint: 1,None
			height: self.minimum_height
			RelativeLayout:
				size_hint: None, None
				width: app.window.width/5
				height: self.width
				FitImage:
					allow_stretch: True
					source: root.cover
					size_hint: 1,1
				IconButton:
					id: play_button
					icon: 'play' if app.playing_sound and app.playing_sound_source == root.source and app.playing_sound.state== 'stop' else('pause' if app.playing_sound and app.playing_sound_source == root.source else 'play')
					font_size: self.parent.width-dp(15)
					size_hint:1, 1
					halign:'center'
					valign:'middle'
					opacity:1 if self.icon =='play' else 0
					theme_text_color: 'Custom'
					text_color: [1,1,1,.75]
					pos_hint:{'center_y': .5,'center_x': .5}
					on_press: 
						app.play_audio(root.source) if self.icon == 'play' else app.pause_audio()
						app.played_sounds.append([play_button,root.source]) if [play_button,root.source] not in app.played_sounds else app.passs()
						play_button.icon = 'play' if app.playing_sound and app.playing_sound_source == root.source and app.playing_sound.state== 'stop' else('pause' if app.playing_sound and app.playing_sound_source == root.source else 'play')
						print(root.height)
			BoxLayout:
				orientation: 'vertical'
				spacing: dp(0)
				size_hint_y:1
				padding: dp(1)
				BoxLayout:
					size_hint:1,.5
			    	MyTextButton:
			    		text: root.username
			    		font_size: dp(15)
			    		italic: True
				        pos_hint: {'bottom':1}
			    		theme_text_color: 'Custom'
			    		text_color:[0,0,0,.75]
			    		halign: 'center'
			    		shorten: True
			    		shorten_from: 'right'
			    		on_press: app.profile([root.post_info[1],root.post_info[6],root.post_info[7]],root)
			    	MDIconButton:
	    				icon: 'dots-horizontal'	 
	    				pos_hint: {'center_y':.5}
	    				on_press:
	    					app.post_options(root.post_info,root)
	    					print(root.height)
	    		BoxLayout:
					size_hint:1,.5
					MDLabel:
				        text: root.title
				        theme_text_color: 'Custom'
				        font_size: dp(15)
				        pos_hint: {'top':1}
				        text_color:[0,0,0,1]
				        halign: 'center'
				        shorten: True
				        shorten_from: 'right'
				MDTextButton:
					text:root.emotion
					pos_hint:{'right':1}
					custom_color:[0,0,0,.75]
		BoxLayout:
		    padding:dp(1)
	    	size_hint_y: None
			height:dp(50)
			BoxLayout:
				size_hint:None,1
				width: self.minimum_width
			    MDIconButton:
				    icon: 'play'
				    theme_text_color: 'Custom'
					text_color: [.75,0,1,1]
				    pos_hint:{'center_y': .5}
				    on_press:
				MDLabel:
					text: '8'#edit size to be texture_size and multiline to be false
			Widget:
				size_hint_x:.05
		    BoxLayout:
				size_hint:None,1
				width: self.minimum_width
				HeartIcon:
					pos_hint: {'center_y':.5}
					id: like_icon
					on_release:
						app.like_post(root.post_info,root)
				MDLabel:
					text: str(root.likes) if root.likes>0 else ''
					max_lines:1
			Widget:
				size_hint_x:.05
			BoxLayout:
				size_hint:None,1
				width: self.minimum_width
			    MDIconButton:
				    icon: 'comment-processing'
				    theme_text_color: 'Custom'
					text_color: [.75,0,1,1]
				    pos_hint:{'center_y': .5}
				    on_press:
				    	app.comments(root.post_info,root)
				MDLabel:
					text: str(root.comments) if root.comments>0 else ''
			Widget:
	        RoundImageTouch:
				source: root.profilepic
		        on_press: app.profile([root.post_info[1],root.post_info[6],root.post_info[7]],root)
		        size_hint: None,.75
		        width: self.height
		        pos_hint:{'top': 1}
	BoxLayout:
    	orientation: "vertical"
    	size_hint:1,None
    	spacing: dp(0)
    	padding: dp(5)
		id: post_info
		height: root.info
    	BoxLayout:
    		id: caption_lay
			size_hint:1,None
			height:self.minimum_height
	    	DynamicLabel:
	    		id: caption
	    		size_hint_y: None
	    		text_size: None, None
	    		text: 'Caption '
	    		shorten: False
	    		shorten_from:'right'
	    	MDTextButton:
	    		id: caption_button
	    		text:'More' if caption.shorten == True else 'Less'
	    		size_hint:None,None
	    		size: dp(40),dp(20)
	    		custom_color: [.1,.1,.1,.75]
	    		pos_hint:{'right':1,'bottom':1}
	    		on_press:
	    			root.height = root.height+(caption.virtual_height-caption.short_height) if caption.shorten == True else root.height-(caption.virtual_height-caption.short_height)
	    			app.adjust_scroll([root.scroll_layout,(caption.virtual_height-caption.short_height)]) if caption.shorten == True else app.adjust_scroll([root.scroll_layout,(caption.short_height-caption.virtual_height)])
	    			post_info.height = post_info.height+(caption.virtual_height-caption.short_height) if caption.shorten == True else post_info.height-(caption.virtual_height-caption.short_height)
	    			caption.height = caption.virtual_height if caption.shorten == True else caption.short_height
	    			caption.shorten = False if caption.shorten == True else True

<VideoLayout>
	id:post_card
    orientation: 'vertical'
    spacing: dp(1)
    padding: dp(0)
    post_image: ''
    info: 
    height: root.virtual_height + root.info
    size_hint:(None,None)
    width: app.window.width
    previous_dialog: None
    pos_hint:{'center_x': .5}
    username: ""
    category: ""
    caption: ""	
    likes: ""
    comments: ""
    duration: ""
    comment_1: ""
    comment_2: ""
    BoxLayout:
    	orientation: "horizontal"
    	size_hint:1, None
    	height: dp(55)
    	padding:dp(1)
    	BoxLayout:
    		orientation: 'vertical'
    		size_hint: None,1
    		width: (app.window.width*0.5)-((dp(50))/2)
	    	MyTextButton:
	        	text: root.username
	        	theme_text_color: 'Custom'
	        	halign: 'center'
			    text_color:[.1,0,.2,1]
	        	font_size: dp(18)
	        	shorten: True
	        	shorten_from: 'right'
	        	on_press: app.profile([root.post_info[1],root.post_info[6],root.post_info[7]],root)
	        MDLabel:
	        	id: emotion
	        	text: root.emotion
	        	font_size: dp(15)
	        	theme_text_color: 'Custom'
	        	halign: 'center'
			    text_color:[0,0,0,.75]
	        	shorten: True
	        	shorten_from: 'right'
        RoundImageTouch:
	        source: root.profilepic
	        on_press: app.profile([root.post_info[1],root.post_info[6],root.post_info[7]],root)
	        size_hint: None,None
	        pos_hint: {'center_y':.5}
	        size: dp(50),dp(50)
	    Widget:
    	MDIconButton:
    		icon: 'dots-vertical'
    		pos_hint: {'center_y':.5}
    		on_press:
    			app.post_options(root.post_info,root)
    			print(root.height)
    RelativeLayout:
    	size_hint: 1, None
	    height: root.post_height
	    PostVideo:
	    	id: post_video
	    	size_hint: 1, None
	    	height: root.post_height
	    	width: root.width
	    	source: root.source
	    	thumbnail: root.thumbnail
	    	root_layout:root
	    	padding:dp(0)
    	BoxLayout:
	    	padding: 0
	    	size_hint_y: None
	    	height: self.minimum_height
	    	width:root.width
	    	pos_hint: {'bottom': 1,'center_x': .5}
	    	Widget:
	    		size_hint_x: None
	    		width: dp(10)
			ImgHeartIcon:
				id: like_icon
				on_release:
					app.like_post(root.post_info,root.likecomment)
			Widget:
    BoxLayout:
    	orientation: "vertical"
    	size_hint:1,None
    	spacing: dp(0)
    	padding: dp(5)
		id: post_info
		height: root.info
    	BoxLayout:
    		id: caption_lay
			size_hint:1,None
			height:self.minimum_height
	    	DynamicLabel:
	    		id: caption
	    		size_hint_y: None
	    		text_size: None, None
	    		text: 'Caption '
	    		shorten: False
	    		shorten_from:'right'
	    	MDTextButton:
	    		id: caption_button
	    		text:'More' if caption.shorten == True else 'Less'
	    		size_hint:None,None
	    		size: dp(40),dp(20)
	    		custom_color: [.1,.1,.1,.75]
	    		pos_hint:{'right':1,'bottom':1}
	    		on_press:
	    			root.height = root.height+(caption.virtual_height-caption.short_height) if caption.shorten == True else root.height-(caption.virtual_height-caption.short_height)
	    			app.adjust_scroll([root.scroll_layout,(caption.virtual_height-caption.short_height)]) if caption.shorten == True else app.adjust_scroll([root.scroll_layout,(caption.short_height-caption.virtual_height)])
	    			post_info.height = post_info.height+(caption.virtual_height-caption.short_height) if caption.shorten == True else post_info.height-(caption.virtual_height-caption.short_height)
	    			caption.height = caption.virtual_height if caption.shorten == True else caption.short_height
	    			caption.shorten = False if caption.shorten == True else True
<PostVideo>
	padding:dp(0)
	RelativeLayout:
    	id: relative_layout
    	size_hint: 1, 1
    	texture: video.texture
    	padding:dp(0)
    	Carousel:
    		size_hint: 1, 1
	    	EffectWidget:
	    		size_hint: 1, 1
		    	id: video_blur
				BlurVideoBg:
					id: blur
					size_hint:1,1
					canvas.before:
						Color:
							rgba: [1,1,1,1]
						Rectangle:
							texture: relative_layout.texture
							pos: self.pos
							size: self.size
					
		Video:#a function on_load to hide thumbnail
			id: video
		    source: root.source
		    state: 'pause'
		    size_hint: 1,1
		    on_state:
		    	app.video_debug(self)
		    	app.video_auto_pause(video,root.root_layout)
		    	print('pause audio if audio') if self.state == 'play' else print('play audio if audio')
		    	app.audio_video_pause() if self.state == 'play' else app.audio_video_play()
		    pos_hint: {'center_x':.5,'center_y':.5}
		    allow_stretch: True
		Image:
			id: thumbnail
			source:root.thumbnail
			size_hint: None,None
		    size: self.parent.size
		    pos_hint: {'center_x':.5,'center_y':.5}
		    allow_stretch: True
		    keep_ratio: False
		    opacity: 1 if video.state == 'stop' else (1 if video.position <= 0 else 0)
		MySpinner:
			pos_hint: {'center_x':.5,'center_y':.5}
			size_hint:None,None
			size: dp(50),dp(50)
			opacity: 0 if playback_icon.opacity != 0 else(1 if video.loaded==False else 0)
		IconButton:
			id: playback_icon
			icon: 'play' if video.state == 'pause' else ('play' if video.state == 'stop' else 'pause')
			theme_text_color: 'Custom'
			text_color:[1,.97,.9,.9]
			pos_hint: {'center_y':.5,'center_x':.5}
			size_hint:None,None
			opacity: 1 if video.state == 'stop' else (1 if video.state == 'pause' else self.opacity)
			size: self.parent.size
			halign: 'center'
			font_size: video.width/4
			on_press:
				app.video_cache() if video.state == 'pause' else app.passs()
				app.video_play(video,thumbnail, playback_icon)
				video.state = 'play' if video.state =='pause' or video.state == 'stop' else 'pause'
				app.playing_video = video
				app.video_auto_pause(video,root.root_layout)
		MDProgressBar:
			max: video.duration
			value: video.position
			size_hint:1,None
			height:dp(7.5)
			color: [.5,0,1,1]
			pos_hint: {'bottom':1,'center_x':.5}
<HomePage>
	name: 'home_screen'
	icon:'home'
	size_hint: 1,1
	pos_hint: {'top':1}
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			size:self.size
			pos:self.pos
	ScreenManager:
		id:screen_manager
		Screen:
			name: 'main'
			id: main
			BoxLayout:
				orientation: "vertical"
				spacing: 0
				MDCard:
					orientation:"horizontal"
					size_hint_y: .1
					pos_hint: {'top':1}
					id: toolbar
					padding: dp(3)
					spacing: dp(5)
					canvas:
				    	Color:
				    		rgba: [1,1,1,.025]
				        Rectangle:
				        	source: 'assets/toolbar.png'
					        size: self.size
					        pos: self.pos
					Widget:
						size_hint_x:0.125
					MDLabel:
						text: "Pulsar"
						font_size:toolbar.height*0.85
						pos_hint:{'center_y':.5}
						bold:True
						halign:'left'
						font_name: 'champ'
						size_hint_x:1
						theme_text_color:'Custom'
						text_color:[.1,0,.2,1]
				BoxLayout:
					orientation: "vertical"
					size_hint_y: .9
					id: home_layout
					spacing: 0
					MyRecycleView:
						id: main_scroll
						size_hint_y: 1
						size_hint_x: 1
						effect_cls: 'ScrollEffect'
					    refresh_callback: app.refresh_callback
					    on_scroll_start: app.scroll_pos_y = args[1].pos[1]
					    on_scroll_move: app.scroll_direction(args[1].pos[1], self.scroll_y, self.refresh_callback, self.root_layout)
					    root_layout: root
					    BoxLayout:
					    	padding: dp(0)
						    spacing: dp(18)
						    id: recycle_layout
						    default_size: None, None
						    default_size_hint:1, None
						    size_hint_y: None
						    height: self.minimum_height
						    orientation: 'vertical'

<ImageScreen>
	name: 'image_screen'
	size_hint: 1, 1
	pos_hint: {'center_y':.5}
	BoxLayout:
		id: post_screen_layout
		orientation:'vertical'
		size_hint: 1, 1
		pos_hint: {'center_x':.5,'center_y':.5}
		spacing: 0
	    MDCard:
	    	size_hint: 1,.1
	    	pos_hint: {'top':1}
	    	id: toolbar
			padding: 3
			spacing: dp(20)
			canvas:
		    	Color:
			    	rgba: [1,1,1,.025]
			    Rectangle:
		        	source: 'assets/toolbar.png'
			        size: self.size
			        pos: self.pos
			MDIconButton:
				icon: 'arrow-left'
				pos_hint: {'center_y':.5}
				on_press:
					app.close_screen(root)
			MDLabel:
				text: 'Post'
				font_size: dp(20)
				italic: True
				halign:'left'
				size_hint_x:1
				pos_hint: {'center_y':.5,'center_x':.5}
		ScrollView:
			size_hint: 1,1
			effect_cls: 'ScrollEffect'
			BoxLayout:
				id: post_scroll
				orientation:'vertical'
				padding: dp(0)
				spacing: dp(15)
				size_hint_y: None
				height: self.minimum_height

<LoginProcess>
	auto_dismiss: False
	background_color:[.7,.3,.05,.05]
	size_hint: .8, None
	height: dp(100)
	pos_hint: {'center_y':.5}
	canvas:
		Color:
			rgba:[1,1,1,1]
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: [10,]
	BoxLayout:
		id: log_process_layout
		size_hint: 1,1
		orientation: 'horizontal'
		pos_hint:{'center_x':.5, 'center_y':.5}
		padding: 30
		spacing: 30
		MySpinner:
			id: log_spinner
			color: [.5,0,1,.75]
			pos_hint:{'center_y':.5}
			size_hint:None,None
			size: dp(30),dp(30)
		MDLabel:
			id: log_message
			halign: 'center'
			text: ""
<LoginProcessNotification>
	id: lay
	size_hint: 1,1
	orientation: 'horizontal'
	pos_hint:{'center_x':.5, 'center_y':.5}
	padding: 5
	spacing: 10
	MDLabel:
		id: log_message
		halign: 'center'
		pos_hint:{'center_x':.5, 'center_y':.5}
		text: ""
		theme_text_color:'Custom'
<Rate>
	height: dp(45)
	BoxLayout:
		padding:5
		Widget:
		MDIconButton:
			id: repost_icon
			icon: "repeat"
			pos_hint:{"center_y": .5}
			theme_text_color: 'Custom'
			text_color:[.75,.1,1,1] if self.icon == 'repeat-once' else [0,0,0,1]
			on_press: 
				app.repost(root.post_info)
				self.icon = 'repeat-once' if self.icon == 'repeat' else 'repeat'
		MDIconButton:
			id: save_icon
			icon: "bookmark-outline"
			pos_hint:{"center_y": .5}
			theme_text_color: 'Custom'
			text_color:[.75,.1,1,1] if self.icon == 'bookmark' else [0,0,0,1]
			on_press: 
				app.save_post(root.post_info)
				self.icon = 'bookmark' if self.icon == 'bookmark-outline' else 'bookmark-outline'
<Time>
	orientation: 'horizontal'
	time:''
	padding:dp(5)
	height:dp(10)
	MDLabel:
		text: root.time
		font_size: dp(12)
		halign: 'right'
		theme_text_color: 'Custom'
		text_color: [0,0,0,.7]
		pos_hint: {'right':1}
	Widget:
		size_hint_x:.15
<LikeComment>
	orientation: 'vertical'
	size_hint: 1, None
	padding: dp(2.5)
	height: dp(60)
	spacing:dp(2.5)
	BoxLayout:
		spacing: 5
		pos_hint: {"center_x":.5}
		Widget:
			size_hint_x:.1
		MDTextButton:
			id: likes_button
			custom_color:[0,0,0,.7]
			pos_hint: {"center_y":.5}
			halign: 'left'
			text:(str(root.likes)+" Like") if root.likes == 1 else ("No Likes"if root.likes == 0 else str(root.likes)+" Likes")
			shorten: True
			shorten_from: 'right'
			on_press: 
				app.likes(root.post_info) if root.likes>0 else app.passs()
		Widget:
		MDTextButton:
			id: comments_button
			custom_color:[0,0,0,.7]
			text: ("View the "+str(root.comments)+" comment") if root.comments == 1 else ("No comments"if root.comments == 0 else "View all "+str(root.comments)+" comments")
			shorten: True
			shorten_from: 'right'
			on_press: 
				app.comments(root.post_info,root) #if root.comments>0 else app.passs()
			pos_hint: {"center_y":.5}
		Widget:
	CommentLay:
		id:comment_lay
		post_info: root.post_info
		likecomment: root
<CommentLay>
	size_hint: 1,None
	height: dp(35)
	Widget:
		size_hint_x:.05
	ButtonBoxLayoutPlain:
		size_hint:1,1
		on_press: app.comments(root.post_info,root.likecomment)
		RoundImageTouch:
			elevation:0
			id: profile_pic
			size_hint: None,1
			width: self.height
		    pos_hint: {'center_y':.5}
		    on_release: app.comments(root.post_info,root.likecomment)
		TextInput:
	    	id: comment
	    	disabled:True
	    	hint_text: 'Make a comment...'
		    border: [0,0,0,0]
		    selection_color: [.7,.3,.05,.4]
		    background_color: [0,0,0,0]
		    pos_hint: {'center_y':.5}
<PinsScreen>
	size_hint: 1, 1
	name: 'pins_screen'
	pos_hint: {'center_y':.5}
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			pos:self.pos
			size: self.size
	BoxLayout:
		orientation:'vertical'
		size_hint: 1, 1
		pos_hint: {'center_x':.5,'center_y':.5}
		MDCard:
			size_hint: 1,.1
			padding: dp(3)
			spacing: dp(5)
			canvas:
		    	Color:
			    	rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
			        size: self.size
		            pos: self.pos
		    MDIconButton:
		    	icon: 'arrow-left'
		    	pos_hint: {'center_y':.5}
		    	on_press:
		    		app.close_screen(root)
		    Widget:
		    	size_hint_x: None
		    	width: dp(5)
		    RoundImageTouch:
				source: root.profile_pic
				size_hint: None,.8
				pos_hint: {'center_y':.5}
				width: self.height
		    MDLabel:
		    	text: root.title
		    	font_size: dp(20)
		    	shorten: True
				shorten_from: 'right'
				size_hint_x:1
		BoxLayout:
			size_hint: 1,1
			orientation: 'vertical'
			ScrollView:
				size_hint: 1,1
				effect_cls: 'ScrollEffect'
				GridLayout:
					id: pins_scroll
					cols:1
					padding: dp(10)
			        spacing: dp(5)
			        size_hint_y: None
			        height: self.minimum_height
<LikeScreen>
	size_hint: 1, 1
	name: 'likes_screen'
	pos_hint: {'center_y':.5}
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			pos:self.pos
			size: self.size
	BoxLayout:
		orientation:'vertical'
		size_hint: 1, 1
		pos_hint: {'center_x':.5,'center_y':.5}
		MDCard:
			size_hint: 1,.1
			padding: dp(3)
			spacing: dp(5)
			canvas:
		    	Color:
			    	rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
			        size: self.size
		            pos: self.pos
		    MDIconButton:
		    	icon: 'arrow-left'
		    	pos_hint: {'center_y':.5}
		    	on_press:
		    		app.close_screen(root)
		    Widget:
		    	size_hint_x: None
		    	width: dp(5)
		    MDLabel:
		    	text: "Likes"
		    	font_size: dp(20)
		    	shorten: True
				shorten_from: 'right'
				size_hint_x:1
		BoxLayout:
			size_hint: 1,1
			orientation: 'vertical'
			ScrollView:
				size_hint: 1,1
				effect_cls: 'ScrollEffect'
				GridLayout:
					id: likes_scroll
					cols:1
					padding: dp(10)
			        spacing: dp(5)
			        size_hint_y: None
			        height: self.minimum_height
<LikesCard>
	height: dp(50)
	size_hint: 1, None
	BoxLayout:
		padding: 5
		spacing: 1
		id: like_card_lay
		RoundImageTouch:
			id: profile_pic
			size_hint: None,None
			size:dp(45),dp(45)
			pos_hint: {'center_y':.5}
			on_press:app.profile(root.user_info,root)
		Widget:
			size_hint_x:.025
		MDLabel:
			id: username
			halign: 'left'
			shorten: True
			shorten_from: 'right'
			bold: True
			font_size: dp(15)
			size_hint_x:1
		PinIcon:
			id: pin_icon
			icon:'pin-off' if not root.pinned else 'pin'
			pos_hint: {'center_y':.5}
	        on_release:
	        	app.pin_user(root.user_info[0],root)
<CommentScreen>
	size_hint: 1, 1
	pos_hint: {'center_y':.5}
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			size: self.size
			pos: self.pos
	BoxLayout:
		orientation:'vertical'
		size_hint: 1, 1
		pos_hint: {'center_x':.5,'center_y':.5}
		MDCard:
			size_hint: 1,None
			height: app.window.height*0.1
			padding: dp(0)
			spacing: dp(5)
			canvas.before:
		    	Color:
			    	rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
			        size: self.size
		            pos: self.pos
		    MDIconButton:
		    	icon: 'arrow-left'
		    	on_release:
		    		print('released')
		    		root.dismiss()
		    	pos_hint: {'center_y':.5}
		    Widget:
		    	size_hint_x: None
		    	width: dp(10)
		    MDLabel:
		    	text: "Comments"
		    	font_size: dp(20)
		    	shorten: True
				shorten_from: 'right'
		BoxLayout:
			size_hint: 1,.8
			orientation: 'vertical'
			ScrollView:
				size_hint: 1,1
				effect_cls: 'ScrollEffect'
				scroll_y:0
				BoxLayout:
					id: comments_scroll
					orientation: 'vertical'
					padding: dp(0)
			        spacing: dp(10)
			        size_hint_y: None
			        height: self.minimum_height
		
		BoxLayout:
			size_hint: 1,None
			height: app.window.height*0.1 if self.minimum_height<(app.window.height*0.1) else self.minimum_height
			padding: 3
			spacing: 10
		    RoundImageTouch:
				id: profile_pic
				size_hint: None, None
				height:dp(50)
				width:self.height
			TypeInput:
				size_hint:1,None
				height: dp(40) if self.minimum_height<dp(40) else self.minimum_height
				pos_hint: {'center_y':.5}
				canvas:
			    	Color:
				    	rgba: [1,1,1,1]
				    RoundedRectangle:
				        size: self.size
			            pos: self.pos
			            radius: [18]
			    canvas.after:
					Color:
						rgba: [0,0,0,.25]
					Line:
						width: dp(1)
						rounded_rectangle: (self.x, self.y, self.width, self.height,\
			                18,18, 18,18,\
			                self.height)
				TextInput:
					id: comment
					size_hint:.8,None
			    	border: [0,0,0,0]
					selection_color: [.7,.3,.05,.4]
					background_color: [0,0,0,0]
					pos_hint: {'center_y':.5}
					height: self.minimum_height if self.minimum_height<(app.window.height*0.3) else app.window.height*0.3
					hint_text: 'Make a comment ...'
		    MDIconButton:
		    	icon: 'send'
		    	on_press: app.comment_on_post(root.info,comment,comments_scroll,root)
		    	canvas.before:
		    		Color:
		    			rgba: [1,.95,.9,1]
		    		Ellipse:
		    			pos:self.pos
		    			size: self.size
<CommentsCard>
	size_hint: 1, None
	height: comment.height+dp(35)+dp(20)
	padding:dp(10)
	BoxLayout:
		padding: dp(1)
		spacing: 1
		pos_hint: {'center_y':.5}
		size_hint: 1, 1
		RoundImageTouch:
			id: profile_pic
			size_hint: None,None
			size: dp(45),dp(45)
			on_press:
				app.profile([root.user_info[0],root.user_info[1],root.user_info[2]],root)
				app.comments_screen.dismiss() if root.user_info[0] != app.user else app.passs
			pos_hint:{'top':1}
		Widget:
			size_hint_x:.025
		BoxLayout:
			orientation: 'vertical'
			padding: dp(1)
			id: comment_layouts
			spacing:dp(5)
			pos_hint: {'top':1}
			size_hint_y: None
			height: dp(20)+comment.height+dp(20)
			MDTextButton:
				id: username
				halign: 'left'
				bold: True
				pos_hint:{'left':1,'center_y':.5}
				custom_color:[0,0,0,1]
				shorten: True
				shorten_from: 'right'
				font_size: dp(13)
				on_press:
					app.profile([root.user_info[0],root.user_info[1],root.user_info[2]],root)
					app.comments_screen.dismiss() if root.user_info[0] != app.user else app.passs
			MDLabel:
	    		size_hint_y: None
	    		text_size: None, None
				halign: 'left'
				id: comment
				size_hint: 1,None
				font_size: dp(13)
			BoxLayout:
				size_hint: 1,None
				spacing: dp(5)
				height:dp(20)
				IconButton:
					pos_hint: {'bottom':1}
					font_size:dp(18)
					size_hint:None,None
					size: dp(20),dp(20)
					icon: 'heart-outline'
					theme_text_color: 'Custom'
					text_color: [.1,.1,.1,.5] if self.icon == 'heart-outline' else [1,.1,.1,1]
					on_release:
						self.icon = "heart" if self.icon == "heart-outline" else "heart-outline"
					valign: 'bottom'
					on_press:
				MDLabel:
					halign: 'left'
					text: '7 likes'
					theme_text_color: 'Custom'
					text_color: [0,0,0,.5]
					font_size: 12
					shorten:True
					shorten_from:'right'
				MDLabel:
					halign: 'right'
					text: root.time
					theme_text_color: 'Custom'
					text_color: [0,0,0,.75]
					font_size: 12
					shorten:True
					shorten_from:'right'
<MyCard>
	canvas.before:
		Color:
			rgba: [1,1,1,1]
        Rectangle:
			size: self.size
            pos: self.pos
<ImgHeartIcon>
	icon: 'heart-outline'
	theme_text_color: 'Custom'
	text_color: [.1,.1,.1,1] if self.icon == 'heart-outline' else [1,.1,.1,1]
	on_release:
		self.icon = "heart" if self.icon == "heart-outline" else "heart-outline"
	canvas.before:
        Color:
            rgba: [1,.85,.5,.25]
        Ellipse:
            pos: self.pos
            size: self.size
<HeartIcon>
	icon: 'heart-outline'
	theme_text_color: 'Custom'
	text_color: [.1,.1,.1,1] if self.icon == 'heart-outline' else [1,.1,.1,1]
	on_release:
		self.icon = "heart" if self.icon == "heart-outline" else "heart-outline"

<CloseIcon>
	icon: 'close'
	theme_text_color: 'Custom'
	text_color: [1,1,1,1]
	canvas.before:
        Color:
            rgba: [.1,.085,.05,.2]
        Ellipse:
            pos: self.pos
            size: self.size
<PinIcon>
	icon: 'pin-off'
	theme_text_color: 'Custom'
	text_color: [0,0,0,1] if self.icon == 'pin-off' else [.75,0,1,1]
    
<MyProfileScreen>
	name: 'my_profile'
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			pos:self.pos
			size: self.size
	ScreenManager:
		id: screen_manager
		Screen:
			id: main
			name: 'main'
			BoxLayout:
				orientation: 'vertical'
				MDCard:
					orientation:"horizontal"
					size_hint_y: .1
					id: toolbar
					padding: 3
					spacing: dp(20)
					canvas:
				    	Color:
				    		rgba: [1,1,1,.025]
				        RoundedRectangle:
				        	source: 'assets/toolbar.png'
					        size: self.size
					        pos: self.pos
					        radius: [0,]
					Widget:
						size_hint_x:.1
					MDLabel:
						id: username
						font_size: dp(20)
						italic: True
						shorten: True
						shorten_from: 'right'
						pos_hint: {'center_y':.5,'center_x':.5}
					MDIconButton:
						icon: 'notification-clear-all'
						size_hint: None,1
						on_press: app.menu()
				ScrollView:
					size_hint: 1,.9
					id: main_scroll
					effect_cls: 'ScrollEffect'
					refresh_callback: root.refresh_function
					on_scroll_start: app.scroll_pos_y = args[1].pos[1]
					on_scroll_move: app.scroll_direction(args[1].pos[1], self.scroll_y, self.refresh_callback, self.root_layout)
					root_layout: root
					BoxLayout:
						orientation:'vertical'
						padding: dp(0)
						spacing: dp(0)
						size_hint_y: None
						height: self.minimum_height
						id: my_profile_layout
						BoxLayout:
							size_hint: 1,None
							padding:dp(10)
							height:app.window.height*0.3
							spacing: dp(10)
							RoundImageTouch:
								id: profilepic
								size_hint: None,None
								size: app.window.height*0.25, app.window.height*0.25
								pos_hint: {'center_y':.5}
							BoxLayout:
								orientation:'vertical'
								size_hint_x:1
								padding:dp(10)
								spacing:dp(5)
								Widget:
									size_hint_y:.15
								MDLabel:
						        	id: fullname
						        	size_hint:1,None
						        	height:dp(25)
						        	halign:'left'
						        	theme_text_color:'Custom'
						        	text_color: [.1,0,.2,1]
							        font_size:dp(18)
							    	bold:True
							    	shorten: True
									shorten_from: 'right'
								MDLabel:
									text:'@'+username.text
						        	size_hint:1,None
						        	height:dp(25)
						        	halign:'left'
						        	theme_text_color:'Custom'
						        	text_color:[0,0,0,.75]
							    	shorten: True
									shorten_from: 'right'
								MDLabel:
									text:'Artist'
						        	size_hint:1,None
						        	height:dp(25)
						        	halign:'left'
						        	theme_text_color:'Custom'
						        	text_color:[0,0,0,.75]
							    	shorten: True
									shorten_from: 'right'
								MDRoundFlatIconButton:
									icon: 'tune'
									text: 'Profile'
									size_hint: None,None
									markup: True
									height:dp(35)
									width: dp(100)
									md_bg_color: [0.0, 0.0, 0.0, 0.0] 
									pos_hint: {'center_y':.5,'left':1}
									theme_text_color: 'Custom'
									text_color: [.1,.1,.1,1]
									on_press:
										app.open_edit_profile()
								Widget:
									size_hint_y:.05
						BoxLayout:
							size_hint: None,None
							pos_hint: {'center_x':.5}
							width: self.minimum_width
							height: dp(60)
							spacing: dp(10)
							ButtonBoxLayoutPlain:
								orientation: 'vertical'
								size_hint:None,1
								width: dp(75)
								on_press:app.pins([app.user,app.profile_pic],'Pins')
								MDLabel:
									bold: True
									text: str(root.pins_count) if root.pins_count>=0 else '-'
									halign: 'center'
								MDLabel:
									text: "Pin" if root.pins_count == 1 else 'Pins'
									shorten: True
									shorten_from: 'right'
									halign: 'center'
							MDSeparator:
								orientation: 'vertical'
							ButtonBoxLayoutPlain:
								orientation: 'vertical'
								size_hint:None,1
								width: dp(75)
								on_press:app.pins([app.user,app.profile_pic],'Pinned')
								MDLabel:
									bold: True
									text: str(root.pinned_count) if root.pinned_count>=0 else '-'
									halign: 'center'
								MDLabel:
									text: "Pinned"
									shorten: True
									shorten_from: 'right'
									halign: 'center'
							MDSeparator:
								orientation: 'vertical'
							ButtonBoxLayoutPlain:
								orientation: 'vertical'
								size_hint:None,1
								width: dp(75)
								MDLabel:
									bold: True
									text: '47'
									halign: 'center'
								MDLabel:
									text: 'Points'
									shorten: True
									shorten_from: 'right'
									halign: 'center'
						BoxLayout:
							orientation: 'vertical'
							id: info_layout
						    height: bio.height+portofolio.height+dp(40)
						    size_hint: 1, None
						    padding: dp(20)
						    spacing: dp(5)
						    MDLabel:
						    	id: bio
						    	size_hint: 1, None
						    	text_size: None, None
						    	halign:'center'
								valign: 'top'
						    LinkTextButton:
						    	id:portofolio
					        	underline: True
						    	halign:'left'
						    	pos_hint:{'center_x':.5}
						        custom_color: [.25,0,.5,1]
						        shorten: True
								shorten_from: 'right'
						FullSeparator:
						MyTabs:
							ButtonBoxLayoutPlain:
								on_press:
									a = scrn_manager.height if scrn_manager.height>=app.window.height*0.81 else app.window.height*0.81
									scrn_manager.current = 'grid_screen'
									grid_height = grid_screen.height if grid_screen.height> app.window.height*0.81 else app.window.height*0.81
									scrn_manager.height = grid_height
									layout.height = grid_height
									app.adjust_scroll_special([my_profile_layout,grid_height-a])
								MDIcon:
									id: grid
									icon: 'grid'
									theme_text_color: 'Custom'
									pos_hint: {'center_y':.5}
									text_color:[.5,0,1,1] if scrn_manager.current == 'grid_screen' else [0,0,0,.75]
									valign: 'middle'
				        			halign: 'center'
							ButtonBoxLayoutPlain:
								on_press:
									a = scrn_manager.height if scrn_manager.height>=app.window.height*0.81 else app.window.height*0.81
									scrn_manager.current = 'repost_screen'
									repost_height = repost_screen.height if repost_screen.height> app.window.height*0.81 else app.window.height*0.81
									scrn_manager.height = repost_height
									layout.height = repost_height
									app.adjust_scroll_special([my_profile_layout,repost_height-a])
								MDIcon:
									id: repeat
									icon: 'repeat'
									theme_text_color: 'Custom'
									pos_hint: {'center_y':.5}
									text_color:[.5,0,1,1] if scrn_manager.current == 'repost_screen' else [0,0,0,.75]
									valign: 'middle'
				        			halign: 'center'
				        	ButtonBoxLayoutPlain:
								on_press:
									a = scrn_manager.height if scrn_manager.height>=app.window.height*0.81 else app.window.height*0.81
									scrn_manager.current = 'saved_screen'
									saved_height = saved_screen.height if saved_screen.height> app.window.height*0.81 else app.window.height*0.81
									scrn_manager.height = saved_height
									layout.height = saved_height
									app.adjust_scroll_special([my_profile_layout,saved_height-a])
								MDIcon:
									id: bookmark
									icon: 'bookmark'
									theme_text_color: 'Custom'
									pos_hint: {'center_y':.5}
									text_color:[.5,0,1,1] if scrn_manager.current == 'saved_screen' else [0,0,0,.75]
									valign: 'middle'
				        			halign: 'center'
				        FullSeparator:
				        BoxLayout:
							id: layout
							size_hint: 1, None
							height: self.minimum_height if self.minimum_height> app.window.height*0.81 else app.window.height*0.81
							ScreenManager:
								id: scrn_manager
								size_hint:1,None
								height: grid_screen.height
								pos_hint:{'top':1}
								Screen:
									id: grid_screen
									name: 'grid_screen'
									size_hint:1,None
									height:grid_layout.height
									pos_hint:{'top':1}
									on_enter:
									GridLayout:
										id: grid_layout
										size_hint:1,None
										pos_hint:{'top':1}
										cols: 3
										spacing: dp(1.2)
										height: self.minimum_height
										
								Screen:
									id: repost_screen
									name: 'repost_screen'
									size_hint:1,None
									height:repost_layout.height
									pos_hint:{'top':1}
									on_enter:
										root.display_reposts() if not root.reposts_active else app.passs()
									GridLayout:
										id: repost_layout
										size_hint_x:1
										pos_hint:{'top':1}
										cols: 3
										spacing: dp(1.2)
										height: self.minimum_height
								Screen:
									id: saved_screen
									name: 'saved_screen'
									size_hint:1,None
									pos_hint:{'top':1}
									height:saved_layout.height
									on_enter:
										root.display_saved() if not root.saved_active else app.passs()
									GridLayout:
										id: saved_layout
										size_hint_x:1
										cols: 3
										pos_hint:{'top':1}
										spacing: dp(1.2)
										height: self.minimum_height
										
<EditProfileScreen>
	size_hint: 1,1
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			size: self.size
			pos: self.pos
	BoxLayout:
		size_hint: 1,1
		orientation: 'vertical'
		spacing: dp(0)
		MDCard:
			orientation:"horizontal"
			size_hint_y: .1
			pos_hint:{'top':1}
			padding: dp(0)
			spacing: dp(5)
			canvas:
		    	Color:
				    rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
				    size: self.size
			        pos: self.pos
			MDIconButton:
		    	icon: 'close'
		    	pos_hint: {'center_y':.5}
		    	custom_color: [1,0,0,1]
				on_press: 
					app.dismiss_edit_profile_screen([profilepic.source, fullname.text, username.text, bio.text, portofolio.text,email.text, phone.text],root)
			Widget:
				size_hint_x:None
				width: dp(5) 
		    MDLabel:
		    	text: 'Edit Profile'
		    	font_size: dp(20)
		    	shorten: True
				shorten_from: 'right'

		    MDTextButton:
		    	text: 'Update'
		    	custom_color: [0,1,0,1] if username.text != '' else [0,.5,0,1]
		    	pos_hint: {'center_y':.5}
		    	on_press: app.edit_profile(profilepic.source, fullname.text, username.text, bio.text, portofolio.text,email.text, phone.text) if username.text != '' else app.passs()
		    Widget:
		    	size_hint_x:None
		    	width: dp(10)
		ScrollView:
			size_hint: 1,1
			effect_cls: 'ScrollEffect'
			BoxLayout:
				orientation: 'vertical'
				size_hint: 1,None
				height: self.minimum_height
				padding: dp(20)
				spacing: dp(20)
				RelativeLayout:
					size_hint: .5,None
					height: self.width
					pos_hint: {'center_x':.5}
					RoundImageTouch:
						id: profilepic
						size_hint: 1,1
					MDIconButton:
						user_font_size: self.parent.height/4
						icon: 'assets/account-camera.png'
						pos_hint: {'center_x':.85,'center_y':.15}
						on_press:app.open_profile_pic_select(profilepic)
				MDTextField:
					id: username
					hint_text: 'Username'
				MDTextField:
					id: fullname
					hint_text: 'Full Name'
				MDTextField:
					id: bio
					hint_text: 'Bio'
					multiline: True
				MDTextField:
					id: portofolio
					hint_text: 'Portofolio/Website'

				Widget:
				MDLabel:
					text: 'Personal'
					font_size: dp(20)
				MDSeparator
				MDTextField:
					id: email
					hint_text: 'Email'
					
				MDTextField:
					id: phone
					hint_text: 'Phone'
					
				MDTextField:
					hint_text: 'Gender'
					text: 'Confidential'


<MenuScreen>
	name: 'menu_screen'
	BoxLayout:
		orientation: "vertical"
		spacing: dp(0)
		size_hint_y: 1
		canvas:
			Color:
				rgba: [1,1,1,1]
			Rectangle:
				pos:self.pos
				size: self.size
		MDCard:
			orientation:"horizontal"
			size_hint_y: .1
			padding: 3
			spacing: dp(5)
			canvas:
		    	Color:
				    rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
				    size: self.size
			        pos: self.pos
			MDIconButton:
		    	icon: 'arrow-left'
		    	pos_hint: {'center_y':.5} 
				on_press: 
					app.root_manager.transition.direction = 'right'
					app.root_manager.current = 'basic_root'
			Widget:
				size_hint_x:None
				width: dp(10)
			MDIconButton:
				icon: 'settings'
		    	pos_hint: {'center_y':.5} 
		    MDLabel:
		    	text: 'Settings'
		    	font_size: dp(20)
		    	shorten: True
		    	shorten_from: 'right'
		ScrollView:
			size_hint: 1,1
			effect_cls: 'ScrollEffect'
			BoxLayout:
				orientation: 'vertical'
				size_hint: 1,None
				height: self.minimum_height
				padding: dp(5)
				spacing: dp(5)
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'account-circle'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'Account'
						shorten: True
		    			shorten_from: 'right'
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'bell-circle'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'Notifications'
						shorten: True
		    			shorten_from: 'right'
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'share-variant'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'Share'
						shorten: True
		    			shorten_from: 'right'
				MDSeparator:
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'google-play'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'Rate'
						shorten: True
		    			shorten_from: 'right'
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'pencil'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'Feedback'
						shorten: True
		    			shorten_from: 'right'
				MDSeparator:
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'lock'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'Privacy'
						shorten: True
		    			shorten_from: 'right'
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'security'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'Security'
						shorten: True
		    			shorten_from: 'right'
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'saxophone'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'Ads'
						shorten: True
		    			shorten_from: 'right'
				MDSeparator:
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'help-circle'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'Help'
						shorten: True
		    			shorten_from: 'right'
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'information'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'About'
						shorten: True
		    			shorten_from: 'right'
				Widget:
					size_hint_y:None
					height:dp(20)
				MDLabel:
					text: 'Logs'
					size_hint:.9,None
					height:dp(24)
					pos_hint:{'right':1}
					font_size: dp(20)
				MDSeparator:
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'account-multiple-plus'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'Add an Account'
						shorten: True
		    			shorten_from: 'right'
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'account-convert'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'Switch Accounts'
						shorten: True
		    			shorten_from: 'right'
				ButtonBoxLayout:
					size_hint: 1,None
					height: dp(50)
					padding:dp(10)
					on_press:app.log_out()
					spacing: dp(10)
					MDIcon: 
						size_hint: None,None
						size: dp(30),dp(30)
						icon: 'logout'
						pos_hint: {'center_y':.5} 
					MDLabel:
						text: 'Log Out'
						shorten: True
		    			shorten_from: 'right'


<ProfileScreen>
	name: 'profile_screen'
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			pos:self.pos
			size: self.size
	on_enter:
	BoxLayout:
		orientation: 'vertical'
		MDCard:
			orientation:"horizontal"
			size_hint_y: .1
			id: toolbar
			padding: 3
			spacing: dp(5)
			canvas:
				Color:
		    		rgba: [1,1,1,.025]
		        RoundedRectangle:
		        	source: 'assets/toolbar.png'
			        size: self.size
					pos: self.pos
			        radius: [0,]
			MDIconButton:
				icon: 'arrow-left'
				pos_hint: {'center_y':.5}
				on_press:
					app.close_screen(root)
			Widget:
				size_hint_x: None
				width: dp(5)
			MDLabel:
				text: root.username
				font_size: dp(20)
				size_hint_x:1
				halign:'left'
				italic: True
				shorten: True
		    	shorten_from: 'right'
				pos_hint: {'center_y':.5,'center_x':.5}

		ScrollView:
			size_hint: 1,.9
			id: profile_scroll
			effect_cls: 'ScrollEffect'
			BoxLayout:
				id: profile_scroll_layout
				orientation:'vertical'
				padding: dp(0)
				size_hint_y: None
				height: self.minimum_height
				BoxLayout:
					size_hint: 1,None
					padding:dp(10)
					height:app.window.height*0.3
					spacing: dp(10)
					RoundImageTouch:
						source:root.profile_pic
						size_hint: None,None
						size: app.window.height*0.25, app.window.height*0.25
						pos_hint: {'center_y':.5}
					BoxLayout:
						orientation:'vertical'
						size_hint_x:1
						padding:dp(10)
						spacing:dp(5)
						Widget:
							size_hint_y:.15
						MDLabel:
				        	id: fullname
				        	size_hint:1,None
				        	height:dp(25)
				        	halign:'left'
				        	theme_text_color:'Custom'
				        	text_color:[.1,0,.2,1]
					        font_size:dp(18)
					    	bold:True
					    	shorten: True
							shorten_from: 'right'
						MDLabel:
							text:'@'+root.username
				        	size_hint:1,None
				        	height:dp(25)
				        	halign:'left'
				        	theme_text_color:'Custom'
				        	text_color:[0,0,0,.75]
					    	shorten: True
							shorten_from: 'right'
						MDLabel:
							text:'Artist'
				        	size_hint:1,None
				        	height:dp(25)
				        	halign:'left'
				        	theme_text_color:'Custom'
				        	text_color:[0,0,0,.75]
					    	shorten: True
							shorten_from: 'right'
						MDRoundFlatIconButton:
							icon: 'pin' if root.pinned else ('pin' if root.user in app.live_pinned_users else ('pin-off' if root.user in app.live_unpinned_users else 'pin-off'))
							text: 'Pin' if self.icon == 'pin-off' else 'Pinned'
							size_hint: None,None
							markup: True
							height:dp(35)
							width: dp(80) if self.text == 'Pin' else dp(100)
							md_bg_color: [0.0, 0.0, 0.0, 0.0] if self.icon == 'pin-off' else [1,.75,.25,.75]
							pos_hint: {'center_y':.5}
							theme_text_color: 'Custom'
							text_color: [.1,.1,.1,1] if self.icon == 'pin-off' else [.75,0,1,1]
							on_release:
								app.pin_user(root.info[0],root)
						Widget:
							size_hint_y:.05
				BoxLayout:
					size_hint: None,None
					pos_hint: {'center_x':.5}
					width: self.minimum_width
					height: dp(70)
					spacing: dp(10)
					ButtonBoxLayoutPlain:
						orientation: 'vertical'
						size_hint:None,1
						width: dp(75)
						on_press:app.pins([root.info[0],root.info[2]],'Pins')
						MDLabel:
							bold: True
							text: str(root.pins_count) if root.pins_count>=0 else '-'
							halign: 'center'
						MDLabel:
							text: "Pin" if root.pins_count == 1 else 'Pins'
							shorten: True
							shorten_from: 'right'
							halign: 'center'
					MDSeparator:
						orientation: 'vertical'
					ButtonBoxLayoutPlain:
						orientation: 'vertical'
						size_hint:None,1
						width: dp(75)
						on_press:app.pins([root.info[0],root.info[2]],'Pinned')
						MDLabel:
							bold: True
							text: str(root.pinned_count) if root.pinned_count>=0 else '-'
							halign: 'center'
						MDLabel:
							text: "Pinned"
							shorten: True
							shorten_from: 'right'
							halign: 'center' 
					MDSeparator:
						orientation: 'vertical'
					ButtonBoxLayoutPlain:
						orientation: 'vertical'
						size_hint:None,1
						width: dp(75)
						MDLabel:
							bold: True
							text: str(root.post_count) if root.post_count>=0 else '-'
							halign: 'center'
						MDLabel:
							text: "Post" if root.post_count==1 else 'Posts'
							shorten: True
							shorten_from: 'right'
							halign: 'center'
				BoxLayout:
					id: info_layout
					orientation: 'vertical'
				    size_hint: 1, None
				    height:bio.height+portofolio.height+dp(45)
					padding: dp(20)
				    MDLabel:
						id: bio
				    	size_hint: 1, None
				    	text_size: None, None
				    	text: root.bio
				    	halign:'center'
						valign: 'top'
				    LinkTextButton:
			        	id: portofolio
			        	underline: True
				    	halign:'left'
				    	pos_hint:{'center_x':.5}
				        custom_color: [0,0,.5,1]
				FullSeparator:
				MyTabs:
					ButtonBoxLayoutPlain:
						on_press:
							a = scrn_manager.height if scrn_manager.height>=app.window.height*0.81 else app.window.height*0.81
							scrn_manager.transition.direction = 'right'
							scrn_manager.current = 'grid_screen'
							grid_height = grid_screen.height if grid_screen.height> app.window.height*0.81 else app.window.height*0.81
							scrn_manager.height = grid_height
							layout.height = grid_height
							app.adjust_scroll_special([profile_scroll_layout,grid_height-a])
						MDIcon:
							id: grid
							icon: 'grid'
							theme_text_color: 'Custom'
							pos_hint: {'center_y':.5}
							text_color:[.5,0,1,1] if scrn_manager.current == 'grid_screen' else [0,0,0,.75]
							valign: 'middle'
				        	halign: 'center'
				    ButtonBoxLayoutPlain:
						on_press:
							a = scrn_manager.height if scrn_manager.height>=app.window.height*0.81 else app.window.height*0.81
							scrn_manager.transition.direction = 'left'
							scrn_manager.current = 'repost_screen'
							repost_height = repost_screen.height if repost_screen.height> app.window.height*0.81 else app.window.height*0.81
							scrn_manager.height = repost_height
							layout.height = repost_height
							app.adjust_scroll_special([profile_scroll_layout,repost_height-a])
						MDIcon:
							id: repeat
							icon: 'repeat'
							theme_text_color: 'Custom'
							pos_hint: {'center_y':.5}
							text_color:[.5,0,1,1] if scrn_manager.current == 'repost_screen' else [0,0,0,.75]
							valign: 'middle'
			        		halign: 'center'
				FullSeparator:
				BoxLayout:
					id: layout
					size_hint: 1, None
					pos_hint:{'top':1}
					height: self.minimum_height if self.minimum_height> app.window.height*0.81 else app.window.height*0.81
					ScreenManager:
						id: scrn_manager
						size_hint:1,None
						height: grid_screen.height
						pos_hint:{'top':1}
						Screen:
							id: grid_screen
							name: 'grid_screen'
							size_hint:1,None
							height:grid_layout.height
							pos_hint:{'top':1}
							on_enter:
							GridLayout:
								id: grid_layout
								size_hint:1,None
								pos_hint:{'top':1}
								cols: 3
								spacing: dp(1.2)
								height: self.minimum_height
						Screen:
							id: repost_screen
							name: 'repost_screen'
							size_hint:1,None
							height:repost_layout.height
							pos_hint:{'top':1}
							on_enter: root.display_reposts() if not root.reposts_active else app.passs()
							GridLayout:
								id: repost_layout
								size_hint_x:1
								pos_hint:{'top':1}
								cols: 3
								spacing: dp(1.2)
								height: self.minimum_height
	
<MessageScreen>
	name: 'messages_screen'
	size_hint: 1, 1
	pos_hint: {'center_y':.5}
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			size: self.size
			pos: self.pos
	BoxLayout:
		orientation:'vertical'
		size_hint: 1, 1
		pos_hint: {'center_x':.5,'center_y':.5}
		MDCard:
			size_hint: 1,.1
			padding: dp(3)
			spacing: dp(1)
			canvas:
		    	Color:
			    	rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
			        size: self.size
		            pos: self.pos
		    MDIconButton:
		    	icon: 'arrow-left'
		    	on_press:
		    		app.root_manager.transition = sm.SlideTransition()
		    		app.root_manager.transition.direction = 'right'
					app.root_manager.current = 'basic_root'
		    	pos_hint: {'center_y':.5}
		    Widget:
		    	size_hint_x: None
		    	width: dp(15)
		    MDLabel:
		    	text: "Messages"
		    	font_size: dp(20)
		    	shorten: True
		    	shorten_from: 'right'

		    MDIconButton:
		    	icon: 'email-plus'
		    	pos_hint: {'center_y':.5}
		BoxLayout:
			size_hint: None,.9
			width: app.window.width
			orientation: 'vertical'
			ScrollView:
				size_hint: 1,1
				effect_cls: 'ScrollEffect'
				GridLayout:
					id: messages_scroll
					cols:1
					padding: dp(0)
			        spacing: dp(0)
			        size_hint_x: 1
			        size_hint_y: None
			        height: self.minimum_height
<MessagesCard>
	height: dp(80)
	size_hint: None, None
	width: app.window.width
	padding:1
	on_press: app.messaging()
	BoxLayout:
		padding: 1
		spacing: dp(5)
		RoundImageTouch:
			source: "assets/beautiful-931152_1280_tile_crop.png"
			size_hint: None,None
			size: dp(50),dp(50)
			pos_hint: {'center_y':.5}
		BoxLayout:
			orientation: 'vertical'
			padding: 5
			spacing: dp(0)
			size_hint_x:1
			MDLabel:
				text: "Username"
				halign: 'left'
				bold: True
				valign: 'bottom'
				font_size: dp(15)
			MDLabel:
				halign: 'left'
				font_size: dp(15)
				max_lines: 1
				valign: 'top'
				shorten: True
				shorten_from: 'right'
				text: "Message, and this counts the number of characters fitting one line"
		BoxLayout:
			orientation: 'vertical'
			size_hint: None,1
			width: dp(50)
			pos_hint: {'center_x':.5,'center_y':.5}
			MDIconButton:
				icon: 'circle'
				pos_hint: {'center_x':.5}
				user_font_size: dp(15)
				theme_text_color:'Custom'
				text_color: [.75,0,1,1]
			MDLabel:
				halign: 'center'
				text: 'Yesterday'
				theme_text_color:'Custom'
				text_color: [0,0,0,.5]
				font_size: 10
<MessagingScreen>
	name: 'messaging_screen'
	size_hint: 1, 1
	pos_hint: {'center_y':.5}
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			size: self.size
			pos: self.pos
	BoxLayout:
		orientation:'vertical'
		size_hint: 1, 1
		pos_hint: {'center_x':.5,'center_y':.5}
		canvas:
			Color:
		    	rgba: [1,1,1,1]
			Rectangle:
		        size: self.size
		        pos: self.pos
		MDCard:
			size_hint: 1,None
			height:app.window.height*0.1
			padding: dp(1)
			spacing: dp(1)
			canvas:
		    	Color:
			    	rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
			        size: self.size
		            pos: self.pos
		    MDIconButton:
		    	icon: 'arrow-left'
		    	pos_hint: {'center_y':.5}
		    	on_press:
		    		app.root_manager.transition = sm.NoTransition()
					app.root_manager.current = 'messages_screen'
					app.root_manager.remove_widget(root)
					on_press: app.messages()
		    RoundImageTouch:
				source: "assets/andre-rodriges.png"
				size_hint: None,.8
				pos_hint: {'center_y':.5}
				width: self.height
			Widget:
				size_hint_x:None
				width: dp(5)
		    MDLabel:
		    	text: "Username"
		    	font_size: dp(20)
		    	halign: 'left'
		    	shorten: True
		    	shorten_from: 'right'
		    MDIconButton:
		    	icon: 'phone'
		    	pos_hint: {'center_y':.5}
		    MDIconButton:
		    	icon: 'video'
		    	pos_hint: {'center_y':.5}
		    MDIconButton:
		    	icon: 'dots-vertical'
		    	pos_hint: {'center_y':.5}
		BoxLayout:
			size_hint: 1,1
			orientation: 'vertical'
			ScrollView:
				id: messaging_scroll
				effect_cls: 'ScrollEffect'
				scroll_y: 0
		BoxLayout:
			size_hint: 1,None
			height: app.window.height*0.1 if self.minimum_height<(app.window.height*0.1) else self.minimum_height
			padding: dp(2)
			spacing: dp(5)
		    RoundImageTouch:
				id: profile_pic
				size_hint: None, None
				height:dp(50)
				width:self.height
			TypeInput:
				size_hint:1,None
				height: dp(40) if self.minimum_height<dp(40) else (self.minimum_height+dp(5))
				pos_hint: {'center_y':.5}
				canvas:
			    	Color:
				    	rgba: [1,1,1,1]
				    RoundedRectangle:
				        size: self.size
			            pos: self.pos
			            radius: [18]
			    canvas.after:
					Color:
						rgba: [0,0,0,.25]
					Line:
						width: dp(1)
						rounded_rectangle: (self.x, self.y, self.width, self.height,\
			                18,18, 18,18,\
			                self.height)
				TextInput:
					id: caption
					size_hint:.8,None
			    	border: [0,0,0,0]
					selection_color: [.7,.3,.05,.4]
					background_color: [0,0,0,0]
					pos_hint: {'center_y':.5}
					height: (self.minimum_height+dp(5)) if (self.minimum_height+dp(5))<(app.window.height*0.3) else app.window.height*0.3
					hint_text: 'Write a message...'
		    MDIconButton:
		    	icon: 'send'
		    	canvas.before:
		    		Color:
		    			rgba: [1,.95,.9,1]
		    		Ellipse:
		    			pos:self.pos
		    			size: self.size
<MessageLabel>
	canvas.before:
		Color:
			rgba: [1,1,1,1]
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius:[10]
	canvas:
		Color:
			rgba: root.color
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius:[10]
	canvas.after:
		Color:
			rgba: [0,0,0,.5]
		Line:
			width: 1
			rounded_rectangle: (self.x, self.y, self.width, self.height,\
                10,10, 10,10,\
                self.height)

<RefreshSpinner>

    AnchorLayout:
        id: body_spinner
        size_hint: None, None
        size: dp(46), dp(46)
        y: Window.height
        pos_hint: {'center_x': .5}
        anchor_x: 'center'
        anchor_y: 'center'

        canvas:
            Color:
                rgba: [1,.95,.9,.75]
            Ellipse:
                pos: self.pos
                size: self.size
        MDSpinner:
            id: spinner
            size_hint: None, None
            size: dp(30), dp(30)
            color: .5, 0, 1, 1
<TagCard>
	markup: True
	text_size:None, None 
	size_hint_y:None
	on_ref_press: app.open_tag_screen(args[1])
<ChallengeScreen>
	name: 'challenges_screen'
	icon: 'certificate'
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			pos:self.pos
			size: self.size
	ScreenManager:
		id: screen_manager
		Screen:
			id: main
			name:'main'
			BoxLayout:
				orientation: "vertical"
				size_hint_y: 1
				spacing: dp(0)
				ScrollView:
					id: main_scroll
					size_hint: 1,1
					effect_cls: 'ScrollEffect'
					BoxLayout:
						id: v_scroll
						size_hint: 1,None
						height: self.minimum_height
						orientation: 'vertical'
						spacing: dp(20)
						RelativeLayout:
							size_hint: 1,None
							height:self.width*0.6
							Carousel:
								id: image_carousel
								loop:True
								size_hint: 1,1
								FitImage:
									source: 'assets/capture1.jpg'
									size_hint: 1,1
								FitImage:
									source: 'assets/capture11.jpg'
									size_hint: 1,1
								FitImage:
									source: 'assets/capture18.jpg'
									size_hint: 1,1
								FitImage:
									source: 'assets/capture20.jpg'
									size_hint: 1,1
								FitImage:
									source: 'assets/capture22.jpg'
									size_hint: 1,1
							BoxLayout:
								size_hint: None,None
								width:self.minimum_width
								pos_hint:{'bottom':1,'center_x':.5}
								spacing: dp(10)
								MDIcon:
									icon: 'circle'
									num: 0
									size_hint:None,None
									size:dp(20),dp(20)
									font_size: dp(15)
									theme_text_color: 'Custom'
									text_color: [0,1,0,.5] if image_carousel.index == int(self.num) else [0,0,0,.5]
								MDIcon:
									icon: 'circle'
									num: 1
									font_size: dp(15)
									size_hint:None,None
									size:dp(20),dp(20)
									theme_text_color: 'Custom'
									text_color: [0,1,0,.5] if image_carousel.index == int(self.num) else [0,0,0,.5]
								MDIcon:
									icon: 'circle'
									num: 2
									font_size: dp(15)
									size_hint:None,None
									size:dp(20),dp(20)
									theme_text_color: 'Custom'
									text_color: [0,1,0,.5] if image_carousel.index == int(self.num) else [0,0,0,.5]

								MDIcon:
									icon: 'circle'
									num: 3
									font_size: dp(15)
									size_hint:None,None
									size:dp(20),dp(20)
									theme_text_color: 'Custom'
									text_color: [0,1,0,.5] if image_carousel.index == int(self.num) else [0,0,0,.5]

								MDIcon:
									icon: 'circle'
									num: 4
									font_size: dp(15)
									size_hint:None,None
									size:dp(20),dp(20)
									theme_text_color: 'Custom'
									text_color: [0,1,0,.5] if image_carousel.index == int(self.num) else [0,0,0,.5]
						BoxLayout:
							orientation: 'vertical'
							size_hint: 1,None
							spacing: dp(5)
							padding: dp(5)
							height: challenge_carousel.height+dp(30)
							BoxLayout
								Widget:
									size_hint_x:.05
								MDLabel:
									size_hint_x:1
									text: 'Challenges'
									bold: True
									shorten: True
									shorten_from: 'right'
									theme_text_color: 'Custom'
									text_color: [.25,0,.5,1]
									font_size: dp(24)
								Widget:
								MDTextButton:
									text: 'See all'
									custom_color: [.25,0,.5,1]
									font_size: dp(18)
							Carousel
								id: challenge_carousel
								size_hint: 1, None
								height: (app.window.width/1.75)
								BoxLayout:
									orientation: 'horizontal'
									size_hint: 1,1
									spacing: dp(10)
									padding: dp(5)
									ChallengeCard:
										size_hint: .5, 1
										source: 'assets/capture31.jpg'
										profile_pic:'assets/kitten-1049129_1280_tile_crop.png'
									ChallengeCard:
										size_hint: .5, 1
										source: 'assets/capture30.jpg'
										profile_pic:'assets/my_pic.jpg'
								BoxLayout:
									orientation: 'horizontal'
									size_hint: 1,1
									spacing: dp(10)
									padding: dp(5)
									ChallengeCard:
										size_hint: .5, 1
										source: 'assets/capture24.jpg'
										profile_pic:'assets/kivymd_logo.png'
									ChallengeCard:
										size_hint: .5, 1
										source: 'assets/capture26.jpg'
										profile_pic:'assets/andre-rodriges.png'
<ChallengeCard>	
	on_press: app.challenge_definition()
	orientation:'vertical'
	spacing:dp(5)
	canvas:
		Color:
			rgba: [1,1,1,1]
		RoundedRectangle:
			size: self.size
			pos: self.pos
			radius: [0,0,10,10]
	RelativeLayout:
		size_hint:1,None
		height:root.width/1.25 + root.width * 0.2
		FitImage:
			allow_stretch: True
			source: root.source
			size_hint: 1,None
			pos_hint:{'top':1}
			height: self.width/1.25
			
		RoundImage:
			source: root.profile_pic
			size_hint: .4,None
			height: self.width
			pos_hint:{'center_x':.5,'bottom':1}
	MDLabel:
		text: 'Challenge name'
		shorten: True
		bold: True
		theme_text_color: 'Custom'
		text_color: [.1,0,.2,1]
		font_size: dp(18)
		height: dp(20)
		halign: 'center'
		shorten_from: 'right'
		pos_hint: {'bottom':1}

<ChallengeLayout>
	orientation:'vertical'
	size_hint:1,None
	height: self.minimum_height
	BoxLayout
		size_hint:1,None
		height: dp(30)
		Widget:
			size_hint_x:.05
		MDLabel:
			size_hint_x:1
			text: '#Challenge Name'
			bold: True
			shorten: True
			shorten_from: 'right'
			theme_text_color: 'Custom'
			text_color: [.25,0,.5,1]
			font_size: dp(20)
		MDIconButton:
			icon: 'more'
			user_font_size: dp(35)
			theme_text_color: 'Custom'
			text_color: [1,.75,.25,1]
			font_size: dp(15)
			pos_hint: {'center_y':.5}
	Carousel:
		size_hint:1,None
		height: self.width/2
		ChallengePostLayout:
		ChallengePostLayout:
<ChallengePostLayout>
	spacing:dp(10)
	padding:dp(5)
	ChallengePostCard:
		size_hint:.5,1
	ChallengePostCard:
		size_hint:.5,1	

<ChallengePostCard>:
	RelativeLayout:
		size_hint:1,1
		FitImage:
			size_hint:1,1
			source:'assets/images (15).jpg'
		BoxLayout:
			size_hint:1,None
			height:dp(25)
			pos_hint:{'center_x':.5,'bottom':1}
			canvas:
				Color:
					rgba:[0,0,0,.5]
				Rectangle:
					pos: self.pos
					size: self.size
			Label:
				size_hint:1,None
				height:dp(25)
				shorten: True
				bold:True
				shorten_from:'right'
				font_size:dp(20)
				halign:'center'
				text:'Username'



<MyTabs@GridLayout>
	rows: 1
	size_hint: 1,None
	height: dp(50)
	canvas:
		Color:
			rgba: [1,1,1,.075]
		Rectangle:
			pos:self.pos
			size: self.size	
<ChallengeDefinition>
	name:'challenge_definition'
	BoxLayout:
		orientation: 'vertical'
		RelativeLayout:
			size_hint: 1, 1
			ScrollView:
				size_hint: 1,1
				id: challenge_definition_scroll
				effect_cls: 'ScrollEffect'
				BoxLayout:
					id: challenge_definition_layout
					orientation:'vertical'
					padding: dp(0)
					spacing: dp(0)
					size_hint_y: None
					height: self.minimum_height
					FitImage:
						id: challenge_image
						source: 'assets/capture34.jpg'
						size_hint: 1,None
						height: self.width/1.5
						allow_stretch: True
					Widget:
						size_hint_y: None
						height: dp(1)
					BoxLayout:
						id: description_layout
						orientation: 'vertical'
						size_hint: 1,None
						height: dp(60)+description.height
						padding: dp(10)
						spacing:dp(10)
						pos_hint: {'bottom':1}
						MDLabel:
							id: description
							size_hint_y: None
		    				text_size: None, None
							text:"Description... \\nThe Tossie Slide Dance is trending. \\nTry it and make our day. \\nDon't spoil the fun"
							halign:'left'
							valign: 'top'
						BoxLayout:
							size_hint: 1,None
							height: dp(35)
							padding: dp(5)
							pos_hint: {'bottom':1}
							MDLabel:
								text: 'Date due'
								shorten: True
								shorten_from: 'right'
							Widget:
							MDRoundFlatIconButton:
								text: 'Post'
								size_hint_y: None
								width:dp(100)
								height: dp(35)
								pos_hint: {'center_y':.5}
								icon: 'postage-stamp'
					FullSeparator:
					MyTabs:
						ButtonBoxLayoutPlain:
							MDTextButton:
								id: recent_tab
								size_hint: .5,1
								text: 'Recent'
								halign: 'center'
								font_size: dp(20)
								shorten: True
								shorten_from: 'right'
								bold: True if scrn_manager.current == 'tecent_screen' else False
								custom_color: [.25,0,.5,1] if scrn_manager.current == 'recent_screen' else [0,0,0,1]
								pos_hint: {'center_y':.5}
								on_press:
									a = scrn_manager.height if scrn_manager.height>=app.window.height*0.81 else app.window.height*0.81
									scrn_manager.transition.direction = 'right'
									scrn_manager.current = 'recent_screen'
									recent_height = recent_screen.height if recent_screen.height> app.window.height*0.81 else app.window.height*0.81
									scrn_manager.height = recent_height
									layout.height = recent_height
									app.adjust_scroll_special([challenge_definition_layout,recent_height-a])
					    ButtonBoxLayoutPlain:
							MDTextButton:
								id: trending_tab
								size_hint: .5,1
								text: 'Trending'
								halign: 'center'
								font_size: dp(20)
								shorten: True
								shorten_from: 'right'
								bold: True if scrn_manager.current == 'trending_screen' else False
								custom_color: [.25,0,.5,1] if scrn_manager.current == 'trending_screen' else [0,0,0,1]
								pos_hint: {'center_y':.5}
								on_press:
									a = scrn_manager.height if scrn_manager.height>=app.window.height*0.81 else app.window.height*0.81
									scrn_manager.transition.direction = 'left'
									scrn_manager.current = 'trending_screen'
									trending_height = trending_screen.height if trending_screen.height> app.window.height*0.81 else app.window.height*0.81
									scrn_manager.height = trending_height
									layout.height = trending_height
									app.adjust_scroll_special([challenge_definition_layout,trending_height-a])
					FullSeparator:
					BoxLayout:
						id: layout
						size_hint: 1, None
						pos_hint:{'top':1}
						height: self.minimum_height if self.minimum_height> app.window.height*0.81 else app.window.height*0.81
						ScreenManager:
							id: scrn_manager
							size_hint:1,None
							height: recent_screen.height
							pos_hint:{'top':1}
							Screen:
								id: recent_screen
								name: 'recent_screen'
								size_hint:1,None
								height:grid_layout.height
								pos_hint:{'top':1}
								on_enter:
								GridLayout:
									id: grid_layout
									size_hint:1,None
									pos_hint:{'top':1}
									cols: 3
									spacing: dp(1.2)
									height: self.minimum_height
							Screen:
								id: trending_screen
								name: 'trending_screen'
								size_hint:1,None
								height:repost_layout.height
								pos_hint:{'top':1}
								on_enter:
								GridLayout:
									id: repost_layout
									size_hint_x:1
									pos_hint:{'top':1}
									cols: 3
									spacing: dp(1.2)
									height: self.minimum_height
									ImageTouch:
										source: 'assets/my_pic.jpg'
										size_hint:None,None
										width: app.window.width/3
										height: self.width/self.image_ratio
									ImageTouch:
										source: 'assets/my_pic.jpg'
										size_hint:None,None
										width: app.window.width/3
										height: self.width/self.image_ratio
									ImageTouch:
										source: 'assets/my_pic.jpg'
										size_hint:None,None
										width: app.window.width/3
										height: self.width/self.image_ratio
			BoxLayout:
				orientation:"horizontal"
				size_hint_y: .1
				id: toolbar
				padding: dp(3)
				pos_hint: {'top':1}
				spacing: dp(5)
				canvas.before:
			    	Color:
					    rgba: [1,1,1,(0.75*(1-challenge_definition_scroll.scroll_y)*challenge_definition_layout.height)/(app.window.width/1.5)] if ((1-challenge_definition_scroll.scroll_y)*challenge_definition_layout.height)<(app.window.width) else [1,1,1,1]
				    Rectangle:
					    size: self.size
				        pos: self.pos
				canvas:
			    	Color:
					    rgba: [1,1,1,(0.025*(1-challenge_definition_scroll.scroll_y)*challenge_definition_layout.height)/(app.window.width/1.5)] if ((1-challenge_definition_scroll.scroll_y)*challenge_definition_layout.height)<(app.window.width) else [1,1,1,0.025]
				    Rectangle:
				    	source: 'assets/toolbar.png'
					    size: self.size
				        pos: self.pos
				MDIconButton:
					icon: 'arrow-left'
					pos_hint: {'center_y':.5}
					on_press:
						root.manager.remove_widget(root)
				Widget:
					size_hint_x:None
					width: dp(10)
				MDLabel:
					text: '#Toosie Slide Challenge'
					font_size: dp(20)
					shorten: True
				    shorten_from: 'right'
					italic: True
					pos_hint: {'center_y':.5,'center_x':.5}
<MyGalaxy>
	name:'my_galaxy'
	icon: 'earth'
	
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			pos:self.pos
			size: self.size
	ScreenManager:
		id: screen_manager
		Screen:
			name: 'main'
			id: main
			BoxLayout:
				orientation: "vertical"
				size_hint_y: 1
				id: galaxy_layout
				spacing: 0
				padding:dp(0)
				ScrollView:
					size_hint: 1, 1
					effect_cls: 'ScrollEffect'
					id: main_scroll
					BoxLayout:
						orientation: 'vertical'
						size_hint: 1,None
						id: main_scroll_layout
						height: self.minimum_height
						spacing: dp(0)
						padding: dp(0)
						BoxLayout:
							orientation:"horizontal"
							size_hint_y: None
							height: dp(56)
							id: toolbar
							padding: dp(3)
							spacing: dp(5)
							Widget:
								size_hint_x:None
								width: dp(10)
							MDLabel:
								text: 'My Galaxy'
								font_size: dp(30)
								theme_text_color: 'Custom'
								text_color:[.1,0,.2,1]
								bold: True
								pos_hint: {'center_y':.5,'center_x':.5}
							MDIconButton:
								icon:'magnify'
								pos_hint: {'center_y':.5}
								on_press: app.open_search_screen()
						BoxLayout:
							size_hint:1,None
							height:dp(45)
							spacing: dp(7.5)
							padding: dp(5)
							MyGalaxyTags:
								id:personalised_tag
								height: dp(35)
								pos_hint: {'center_y':.5}
								group: 'galaxy'
								icon: 'account'
								text: 'Personalised'
							MyGalaxyTags:
								height: dp(35)
								pos_hint: {'center_y':.5}
								group: 'galaxy'
								icon: 'google-earth'
								text: 'Trending'
							MyGalaxyTags:
								height: dp(35)
								pos_hint: {'center_y':.5}
								group: 'galaxy'
								icon: 'music'
								text: 'Latest'
						Widget:
							size_hint_y:None
							height:dp(20)
						BoxLayout:
							id:my_galaxy_layout
							orientation: 'vertical'
							size_hint: 1,None
							height: self.minimum_height
							spacing: dp(30)
							padding: dp(0)
<MyGalaxyTags>
	theme_text_color: 'Custom'
	text_color:[1,1,1,1] if self.state == 'down' else [.75,0,1,1]
	md_bg_color:[.85,.1,1,.85] if self.state== 'down' else[0,0,0,0]
<MyGalaxyGallery>
	orientation:'vertical'
	size_hint: 1,None
	spacing:dp(1)
	height: self.minimum_height
	BoxLayout:
		padding: dp(1)
		id: title
		size_hint_y:None
		height: dp(25)
		Widget:
			size_hint_x:.05
		MDLabel:
			size_hint_x:1
			halign:'left'
			text: 'Collections'
			bold: True
			shorten: True
			shorten_from: 'right'
			theme_text_color: 'Custom'
			text_color: [.25,0,.5,1]
			font_size: dp(24)
		
	Widget:
		size_hint_y:None
		height:dp(5)
	BoxLayout:
		orientation: 'horizontal'
		size_hint: 1,None
		height: self.width*(2/3)
		spacing: dp(1)
		padding:dp(0)
		FitImageTouch:
			size_hint: .2/3,None
			height: self.width
			source:root.collection[0][1]
			on_press:app.my_galaxy_open_post(root.collection[0])
		BoxLayout:
			size_hint: .1/3, 1
			height: self.width
			spacing: dp(1)
			orientation:'vertical'
			FitImageTouch:
				size_hint:1,.5
				source: root.collection[2][1]
				on_press:app.my_galaxy_open_post(root.collection[2])
			FitImageTouch:
				size_hint:1,.5
				source: root.collection[3][1]
				on_press:app.my_galaxy_open_post(root.collection[3])
	BoxLayout:
		size_hint: 1, None
		height: self.width/3
		spacing: dp(1)
		FitImageTouch:
			size_hint:None,1
			width:app.window.width/3 - dp(1)
			source: root.collection[4][1]
			on_press:app.my_galaxy_open_post(root.collection[4])
		FitImageTouch:
			size_hint:None,1
			width: app.window.width/3 - dp(0.5)
			source: root.collection[5][1]
			on_press:app.my_galaxy_open_post(root.collection[5])
		FitImageTouch:
			size_hint:.1/3,1
			source: root.collection[6][1]
			on_press:app.my_galaxy_open_post(root.collection[6])
	BoxLayout:
		orientation: 'horizontal'
		size_hint: 1,None
		height: self.width*(2/3)
		spacing: dp(1)
		padding:dp(0)
		BoxLayout:
			size_hint: .1/3, 1
			height: self.width
			spacing: dp(1)
			orientation:'vertical'
			FitImageTouch:
				size_hint:1,.5
				source: root.collection[7][1]
				on_press:app.my_galaxy_open_post(root.collection[7])
			FitImageTouch:
				size_hint:1,.5
				source: root.collection[8][1]
				on_press:app.my_galaxy_open_post(root.collection[8])
		FitImageTouch:
			size_hint: .2/3,None
			height: self.width
			source:root.collection[1][1]
			on_press:app.my_galaxy_open_post(root.collection[1])
							
<PeopleLayout>
	orientation:'vertical'
	size_hint: 1,None
	height: people_carousel.height+dp(30)
	BoxLayout:
		padding: dp(1)
		height:dp(30)
		Widget:
			size_hint_x:.05
		MDLabel:
			size_hint_x:1
			text: root.title
			bold: True
			shorten: True
			shorten_from: 'right'
			theme_text_color: 'Custom'
			text_color: [.25,0,.5,1]
			font_size: dp(24)
	Carousel:
		loop: False
		id: people_carousel
		size_hint: 1,None
		height:	(app.window.width/2)+dp(30)
		
<MyGalaxyVideos>
	orientation:'vertical'
	size_hint: 1,None
	height: carousel.height +dp(30) 
	BoxLayout:
		padding: dp(1)
		height:dp(30)
		Widget:
			size_hint_x:.05
		MDLabel:
			size_hint_x:1
			text: 'Videos'
			bold: True
			shorten: True
			shorten_from: 'right'
			theme_text_color: 'Custom'
			text_color: [.25,0,.5,1]
			font_size: dp(24)
	Carousel:
		id: carousel
		size_hint:1,None
		on_index:
			before = root.height
			before_parent = app.my_galaxy.ids.main_scroll_layout.height
			self.height = self.current_slide.height+dp(5)
			app.my_galaxy.ids.my_galaxy_layout.height=(app.my_galaxy.ids.my_galaxy_layout.height+root.height-before) if self.index !=0 else app.my_galaxy.ids.my_galaxy_layout.height
			app.adjust_scroll([app.my_galaxy.ids.main_scroll_layout,(root.height-before)])
			app.my_galaxy.video_active = False if self.index == 0 else True
<DisplayingVideo>
	padding:dp(0)
	RelativeLayout:
    	id: relative_layout
    	size_hint: 1, 1
    	texture: video.texture
    	padding:dp(0)
    	Carousel:
    		size_hint: 1, 1
	    	EffectWidget:
	    		size_hint: 1, 1
		    	id: video_blur
				BlurVideoBg:
					id: blur
					size_hint:1,1
					canvas.before:
						Color:
							rgba: [1,1,1,1]
						Rectangle:
							texture: relative_layout.texture
							pos: self.pos
							size: self.size
					
		Video:
			id: video
		    source: root.source
		    state: root.state if app.my_galaxy.video_active == True else 'pause'
		    on_state:
		    	app.playing_video = self if self.state == 'play' else app.passs()
			    app.video_debug(self)
			    app.video_auto_pause(self,root.root_layout)
			    print(app.stopped_playing_sound)
			    print('pause audio if audio') if self.state == 'play' else print('play audio if audio')
			    app.audio_video_pause() if self.state == 'play' else app.audio_video_play()
			    print(app.stopped_playing_sound)
		    size_hint: 1,1
		    pos_hint: {'center_x':.5,'center_y':.5}
		    allow_stretch: True
		Image:
			id: thumbnail
			source:root.thumbnail
			size_hint: None,None
		    size: self.parent.size
		    pos_hint: {'center_x':.5,'center_y':.5}
		    allow_stretch: True
		    keep_ratio: False
		    opacity: 1 if video.state == 'stop' else (1 if video.loaded == False else 0)
		MySpinner:
			pos_hint: {'center_x':.5,'center_y':.5}
			size_hint:None,None
			size: dp(50),dp(50)
			opacity: 0 if playback_icon.opacity != 0 else(1 if video.loaded==False else 0)
		IconButton:
			id: playback_icon
			icon: 'play' if video.state == 'pause' else ('play' if video.state == 'stop' else 'pause')
			theme_text_color: 'Custom'
			text_color:[1,.97,.9,.9]
			pos_hint: {'center_y':.5,'center_x':.5}
			size_hint:None,None
			opacity: 1 if video.state == 'stop' else (1 if video.state == 'pause' else 0)
			size: self.parent.size
			halign: 'center'
			font_size: video.width/4
			on_press:
				app.video_cache() if video.state == 'pause' else app.passs()
				app.video_play(video,thumbnail, playback_icon)
				video.state = 'play' if video.state =='pause' else 'pause'
				app.playing_video = video
				print(app.playing_video)
<VideoDisplayUnit>
	orientation:'vertical'
	size_hint:1,None
	height:post_video.height+dp(50)
	pos_hint: {'top':1,'center_x':.5}
	RelativeLayout:
		size_hint:1,None
		height:post_video.height
		DisplayingVideo:
			id: post_video
	    	size_hint: 1, None
	    	height: self.width/root.info[4]
			source: root.source
		    thumbnail: root.thumbnail
		    state: 'play' if app.root_screen.current == 'my_galaxy' and root.base.index == root.num else 'pause'
		    index: root.num
		    pos_hint:{'center_y':.5,'center_x':.5}
		    root_layout: root.base.parent.parent
		    padding:dp(0)
		BoxLayout:
			size_hint:1,None
			height: self.minimum_height
			BoxLayout:
				orientation: 'vertical'
				size_hint: None,None
				size: app.window.width,self.minimum_height
				pos_hint: {'bottom':1,'left':1}
				padding:dp(5)
				BoxLayout:
					orientation: 'vertical'
					size_hint: None,None
					size: app.window.width,self.minimum_height
					padding: dp(10)
				
				BoxLayout:
					size_hint:1,None
					height: dp(50)
					padding:dp(2.5)
					spacing:dp(5)
					RoundImageTouch:
						size_hint:None,1
						width:self.height
						source: root.info[6]
						on_press:app.profile([root.info[1],root.info[5],root.info[6]],root)
					BoxLayout:
						size_hint:1,1
						MDTextButton:
							size_hint: None,1
							text: root.info[5]
							halign: 'left'
							font_size: dp(15)
							shorten: True
							shorten_from: 'right'
							bold: True
							custom_color: [1,1,1,1]
							pos_hint: {'center_y':.5}
							on_press:on_press:app.profile([root.info[1],root.info[5],root.info[6]],root)
					MDRoundFlatIconButton:
						icon: 'pin' if root.pinned else ('pin' if root.info[1] in app.live_pinned_users else ('pin-off' if root.info[1] in app.live_unpinned_users else 'pin-off'))
						text: 'Pin' if self.icon == 'pin-off' else 'Pinned'
						size_hint: None,None
						markup: True
						height:dp(35)
						width: dp(80) if self.text == 'Pin' else dp(100)
						md_bg_color: [0.0, 0.0, 0.0, 0.0] if self.icon == 'pin-off' else [1,.75,.25,.75]
						pos_hint: {'center_y':.5,'center_x':.5}
						theme_text_color: 'Custom'
						text_color: [.1,.1,.1,1] if self.icon == 'pin-off' else [.75,0,1,1]
						on_press:
							app.pin_user(root.info[1],root)
				MDProgressBar:
					max: post_video.ids.video.duration
					value: post_video.ids.video.position
					size_hint:1,None
					height:dp(1)
					color: [.5,0,1,1]
	BoxLayout:
		size_hint:1,None
		height:dp(50)
		MDIconButton:
			icon: root.sub_info[0]
			theme_text_color: 'Custom'
			text_color: [1,0,0,1] if self.icon == 'heart' else [0,0,0,1]
			on_press: 
				app.like_post([root.info[3],root.info[1],root.info[0]],None)
				self.icon = 'heart' if self.icon =='heart-outline' else 'heart-outline'
		MDIconButton:
			icon: 'comment-text'
			theme_text_color: 'Custom'
			text_color: [0,0,0,.75]
			pos_hint:{'center_y':.5}
			on_press:app.comments([None,root.info[1],root.info[0],root.info[7],None,None,root.info[5],root.info[6],None],None)
		Widget:
		MDIconButton:
			id:repost_icon
			icon: root.sub_info[3]
			theme_text_color: 'Custom'
			text_color: [.75,0,1,1] if self.icon == 'repeat-once' else [0,0,0,1]
			on_press:
				app.repost([root.info[3],root.info[1],root.info[0]])
				self.icon = 'repeat-once' if self.icon == 'repeat' else 'repeat'
		MDIconButton:
			id:save_icon
			icon: root.sub_info[4]
			theme_text_color: 'Custom'
			text_color:[0,0,0,1] if self.icon == 'bookmark-outline' else [.75,0,1,1]
			on_press:
				app.save_post([root.info[3],root.info[1],root.info[0]])
				self.icon = 'bookmark' if self.icon == 'bookmark-outline' else 'bookmark-outline'

<PeopleCard>
	size_hint: None, 1
	orientation:'vertical'
	width: (app.window.width/2)-dp(10)
	on_press:
		app.profile([root.info[0],root.info[1],root.info[2]],root)
	canvas:
		Color:
			rgba: [1,1,1,1]
		RoundedRectangle:
			pos:self.pos
			size:self.size
			radius: [0,0,10,10]
	RelativeLayout:
		orientation: 'vertical'
		size_hint: 1,None
		height: ((root.width/2)+root.height)/2
		spacing: dp(0)
		FitImage:
			source:root.cover_image
			size_hint:1,None
			height:root.height/2
			pos_hint:{'top':1}
			canvas.after:
				Color:
					rgba:[1,1,1,.25]
				Rectangle:
					size:self.size
					pos:self.pos
		RoundImage:
			size_hint:.5,None
			allow_stretch:True
			height:self.width
			source: root.profile_pic
			pos_hint: {'center_x':.5,'bottom':1}
	BoxLayout:
		orientation:'vertical'
		size_hint:1,None
		height:dp(70)
		padding:dp(5)
		spacing:dp(5)
		pos_hint:{'bottom':1}
		MDLabel:
			text: root.username
			shorten:True
			shorten_from:'right'
			halign:'center'
			size_hint_x:None
			width:self.parent.width
			theme_text_color: 'Custom'
			text_color:[0,0,0,1]
			font_size:dp(18)

		MDRoundFlatIconButton:
			icon: 'pin' if root.pinned else ('pin' if root.info[0] in app.live_pinned_users else ('pin-off' if root.info[0] in app.live_unpinned_users else 'pin-off'))
			text: 'Pin' if self.icon == 'pin-off' else 'Pinned'
			size_hint: None,None
			markup: True
			height:dp(35)
			width: dp(80) if self.text == 'Pin' else dp(100)
			md_bg_color: [0.0, 0.0, 0.0, 0.0] if self.icon == 'pin-off' else [1,.75,.25,.75]
			pos_hint: {'center_y':.5,'center_x':.5}
			increment_width: dp(2)
			theme_text_color: 'Custom'
			text_color: [.1,.1,.1,1] if self.icon == 'pin-off' else [.75,0,1,1]
			on_press:
				app.pin_user(root.info[0],root)
				
<DiscoverTagsLayout>
	orientation:'vertical'
	size_hint: 1,None
	height: app.window.width+dp(50)
	BoxLayout:
		padding: dp(1)
		height:dp(30)
		Widget:
			size_hint_x:.05
		MDLabel:
			size_hint_x:1
			text: 'Trending Tags'
			bold: True
			shorten: True
			shorten_from: 'right'
			theme_text_color: 'Custom'
			text_color: [.25,0,.5,1]
			font_size: dp(24)
	Carousel:
		loop: False
		id: tags_carousel
		size_hint: 1,None
		height:	app.window.width+dp(20)
<DiscoverTagsCard>
	size_hint: .8, .95
	pos_hint:{'center_x':.5,'top':1}
	canvas:
		Color:
			rgba: [1,1,1,1]
		RoundedRectangle:
			pos:self.pos
			size:self.size
			radius:[0,0,20,20]
	BoxLayout:
		orientation:'vertical'
		size_hint:1,1
		RelativeLayout:
			size_hint:1,None
			height:self.parent.height-dp(35)
			pos_hint:{'top':1}
			BoxLayout:
				orientation: 'vertical'
				size_hint:1,1
				spacing:dp(1)
				FitImage:
					id: cover_img
					size_hint:1,None
					height:self.width/1.5
					source: root.pics[0]
				BoxLayout:
					size_hint:1,None
					height:root.height-(dp(25)+(root.width/1.5))
					spacing:dp(1)
					FitImage:
						size_hint:.5,1
						source: root.pics[1]
					FitImage:
						size_hint:.5,1
						source: root.pics[2]
			BoxLayout:
				size_hint: None,None
				height:dp(45)
				width: self.minimum_width
				pos_hint: {'center_x':.5,'bottom':1}
				MDRoundFlatIconButton:
					icon: 'pin-off'
					text: 'Pin'
					size_hint: None,None
					height:dp(35)
					markup: True
					width: dp(80) if self.text == 'Pin' else dp(100)
					md_bg_color: [0.0, 0.0, 0.0, 0.0] if self.text == 'Pin' else [1,.75,.25,.75]
					pos_hint: {'center_x':.5,'top':1}
					increment_width: dp(2)
					theme_text_color: 'Custom'
					text_color: [1,1,1,1]
					on_press:
						self.icon = 'pin' if self.icon == 'pin-off' else 'pin-off'
						self.text_color = [.75,0,1,1] if self.text_color == [1,1,1,1] else [1,1,1,1]
						self.text = 'Pinned' if self.text=='Pin' else 'Pin'
			MDIconButton:
				icon:'star-outline'
				user_font_size:dp(30)
				pos_hint: {'right':1,'top':1}
				theme_text_color:'Custom'
				text_color:[1,.75,.25,.75] if self.icon =='star' else [0,0,0,1]
				on_press:
					self.icon = 'star' if self.icon == 'star-outline' else 'star-outline'
		MDLabel:
			size_hint:1,None
			height:dp(35)
			font_size:dp(25)
			bold:True
			theme_text_color: 'Custom'
			text_color:[.1,0,.2,1]
			halign:'center'
			shorten:True
			shorten_from: 'right'
			text:root.info
<MyGalaxyPostDisplay>
	orientation:'vertical'
	size_hint:1,None
	height: self.minimum_height
	BoxLayout:
		size_hint: 1,None
		height:dp(30)

		Widget:
			size_hint_x:.05
		MDLabel:
			size_hint_x:1
			text: 'Photos'
			bold: True
			shorten: True
			shorten_from: 'right'
			theme_text_color: 'Custom'
			text_color: [.25,0,.5,1]
			font_size: dp(24)
	Carousel:
		id:photos_carousel
		size_hint:1,None
		height:(self.width*1.2)
<MyGalaxyPostDisplayUnit>
	orientation:'vertical'
	size_hint: .9,(1/1.05)
	pos_hint: {'center_x':.5,'top':1}
	canvas:
		Color:
			rgba: [1,1,1,1]
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius:[0,0,25,25]
	RelativeLayout:
		size_hint:1,None
		height:self.width
		pos_hint:{'top':1}
		FitImage:
			size_hint:1,1
			source:root.info[2]
		RoundImageTouch:
			size_hint:.3,None
			height: self.width
			source: root.info[4]
			pos_hint:{'center_x':.5,'center_y':0}
			on_press:app.profile([root.info[1],root.info[3],root.info[4]],root)
		
		PinIcon:
			id:pin_icon
			user_font_size:dp(30)
			pos_hint:{'top':1,'right':1}
			icon: 'pin' if root.pinned else ('pin' if root.info[1] in app.live_pinned_users else ('pin-off' if root.info[1] in app.live_unpinned_users else 'pin-off'))
			on_release:
	        	app.pin_user(root.info[1],root)
	RelativeLayout:
		size_hint:1,None
		height: root.height-root.width
		pos_hint:{'bottom':1}
		BoxLayout:
			size_hint:1,1
			BoxLayout:
				size_hint:None,None
				width: (root.width/2)-(root.width*0.15)
				height:self.minimum_height
				pos_hint:{'top':1}
				MDIconButton:
					icon: root.sub_info[0]
					theme_text_color: 'Custom'
					text_color: [1,0,0,1] if self.icon == 'heart' else [0,0,0,1]
					on_press: 
						app.like_post([root.info[3],root.info[1],root.info[0]],None)
						self.icon = 'heart' if self.icon =='heart-outline' else 'heart-outline'
				Widget:
					size_hint_x:None
					width:self.parent.width -dp(100)
				MDIconButton:
					icon: 'comment-text'
					theme_text_color: 'Custom'
					text_color: [.75,0,1,1]
					on_press:app.comments([None,root.info[1],root.info[0],root.info[5],None,None,root.info[3],root.info[4],None],None)
				
			Widget:
				size_hint_x:None
				width: (root.width*0.3)
			BoxLayout:
				size_hint:None,None
				width: (root.width/2)-(root.width*0.15)
				height:self.minimum_height
				pos_hint:{'top':1}
				MDIconButton:
					id:repost_icon
					icon: root.sub_info[3]
					theme_text_color: 'Custom'
					text_color: [.75,0,1,1] if self.icon == 'repeat-once' else [0,0,0,1]
					on_press:
						app.repost([root.info[3],root.info[1],root.info[0]])
						self.icon = 'repeat-once' if self.icon == 'repeat' else 'repeat'
				Widget:
					size_hint_x:None
					width:self.parent.width -dp(100)
				MDIconButton:
					id:save_icon
					icon: root.sub_info[4]
					theme_text_color: 'Custom'
					text_color:[0,0,0,1] if self.icon == 'bookmark-outline' else [.75,0,1,1]
					on_press:
						app.save_post([root.info[3],root.info[1],root.info[0]])
						self.icon = 'bookmark' if self.icon == 'bookmark-outline' else 'bookmark-outline'
		BoxLayout:
			size_hint:None,None
			width:self.parent.width-dp(100)
			height:dp(45)
			pos_hint:{'center_x':.5,'bottom':1}
			MDTextButton:
				text: root.info[3]
				bold: True
				shorten:True
				shorten_from:'right'
				halign:'center'
				size_hint_x:1
				custom_color:[.1,0,.2,1]
				font_size:dp(20)
				pos_hint:{'center_x':.5,'center_y':.5}
				on_press:app.profile([root.info[1],root.info[3],root.info[4]],root)
<MyGalaxyAudioDisplay>
	orientation:'vertical'
	size_hint:1,None
	height: app.window.width+dp(30)
	BoxLayout:
		size_hint: 1,None
		height:dp(30)
		Widget:
			size_hint_x:.05
		MDLabel:
			size_hint_x:1
			text: 'Great Sounds'
			bold: True
			shorten: True
			shorten_from: 'right'
			theme_text_color: 'Custom'
			text_color: [.25,0,.5,1]
			font_size: dp(24)

	RelativeLayout:
		size_hint:1,None
		height: app.window.width
		Image:
			id:cover_image
			size_hint:1,1
			allow_stretch: True
			source:root.audio[root.index][3]
			canvas.after:
				Color:
					rgba:[1,1,1,1]
				Rectangle:
					source: 'assets/music_bg2.png'
					size:self.size
					pos: self.pos
		BoxLayout:
			orientation: 'vertical'
			pos_hint: {'top':1}
			size_hint:1,None
			height: dp(60)
			BoxLayout:
				size_hint:1,None
				height:dp(30)
				MDLabel
			    	text: root.audio[root.index][5]
			    	font_size: dp(20)
			    	italic: True
			    	pos_hint: {'bottom':1}
			    	theme_text_color: 'Custom'
			    	text_color:[0,0,0,.75]
			    	halign: 'center'
			    	shorten: True
			    	shorten_from: 'right'
			MDLabel:
				text: root.audio[root.index][4]
		        theme_text_color: 'Custom'
		        font_size: dp(20)
		        pos_hint: {'bottom':1}
		        text_color:[0,0,0,1]
		        halign: 'center'
		        shorten: True
		        shorten_from: 'right'
		BoxLayout:
			orientation: 'vertical'
			size_hint:1,None
			height:dp(110)
			pos_hint:{'bottom':1}
			BoxLayout:
				size_hint:1,None
				height:dp(50)
				Widget:
				MDIconButton:
					pos_hint:{'center_y':.5}
					theme_text_color: 'Custom'
					text_color:[1,1,1,1] if self.icon == 'heart-outline' else [1,.1,.1,1]
					icon: root.sub_info[root.index][0]
					on_press:
						app.like_post([root.audio[root.index][3],root.audio[root.index][1],root.audio[root.index][0]],None)
						self.icon = 'heart' if self.icon == 'heart-outline' else 'heart-outline'
				MDIconButton:
					pos_hint:{'center_y':.5}
					theme_text_color: 'Custom'
					text_color:[1,1,1,1]
					icon: 'comment-processing-outline'
					on_press:app.comments([None,root.audio[root.index][1],root.audio[root.index][0],root.audio[root.index][7],None,None,root.audio[root.index][5],root.audio[root.index][6],None],None)
				MDIconButton:
					pos_hint:{'center_y':.5}
					theme_text_color: 'Custom'
					text_color:[1,1,1,1] if self.icon == 'repeat' else [1,.75,.25,1]
					icon: root.sub_info[root.index][3]
					on_press:
						app.repost([root.audio[root.index][3],root.audio[root.index][1],root.audio[root.index][0]])
						self.icon = 'repeat-once' if self.icon == 'repeat' else 'repeat'
					disabled: False if root.audio[root.index][1] != app.user else True
					opacity:0 if self.disabled else 1
				MDIconButton:
					pos_hint:{'center_y':.5}
					theme_text_color: 'Custom'
					text_color:[1,1,1,1] if self.icon == 'bookmark-outline' else [1,.75,.25,1]
					icon: root.sub_info[root.index][4]
					on_press:
						app.save_post([root.audio[root.index][3],root.audio[root.index][1],root.audio[root.index][0]])
						self.icon = 'bookmark' if self.icon == 'bookmark-outline' else 'bookmark-outline'
					disabled: False if root.audio[root.index][1] != app.user else True
					opacity:0 if self.disabled else 1
				Widget:
			BoxLayout:
				size_hint:1,None
				height:dp(60)
				pos_hint:{'bottom':1}
				Widget:
					size_hint_x:None
					width:dp(10)
				MyGalaxyAudioProfile:
					pinned: root.pinned[root.index]
					size_hint:None,.8
					width:self.height
					pos_hint:{'center_y':.5}
					source: root.audio[root.index][6]
					on_press:app.profile([root.audio[root.index][1],root.audio[root.index][5],root.audio[root.index][6]],self)
				Widget:
					size_hint_x:None
					width:(app.window.width/2)-dp(10+48+75)
				BoxLayout:
					size_hint:None,1
					width:dp(150)
					IconButton:
						pos_hint:{'center_y':.5}
						size_hint:None,None
						size:dp(45),dp(45)
						halign: 'center'
						valign:'middle'
						theme_text_color: 'Custom'
						text_color:[.9,.7,.225,.9] if self.icon == 'skip-previous-outline' else [1,.75,.25,1]
						icon: 'skip-previous-outline' if root.index<=0 else 'skip-previous-circle-outline'
						disabled: False if self.icon == 'skip-previous-circle-outline' else True
						font_size:dp(45)
						on_release:
							app.stopped_playing_sound = None
							app.pause_audio()
							root.index = root.index if root.index<=0 else root.index-1
							app.play_audio(root.source[root.index])
							app.played_sounds.append([play_button,root.source[root.index]]) if [play_button,root.source[root.index]] not in app.played_sounds else app.passs()
							play_button.icon = 'play' if app.playing_sound and app.playing_sound_source == root.source[root.index] and app.playing_sound.state== 'stop' else('pause' if app.playing_sound and app.playing_sound_source == root.source[root.index] else 'play')
					IconButton:
						id:play_button
						pos_hint:{'center_y':.5}
						size_hint:None,None
						size:dp(60),dp(60)
						halign: 'center'
						valign:'middle'
						theme_text_color: 'Custom'
						text_color:[1,.75,.25,1] #play-circle-outline
						icon: 'play' if app.playing_sound and app.playing_sound_source == root.source and app.playing_sound.state== 'stop' else('pause' if app.playing_sound and app.playing_sound_source == root.source else 'play')
						font_size:dp(60)
						on_release:
							app.stopped_playing_sound = None
							app.play_audio(root.source[root.index]) if self.icon == 'play' else app.pause_audio()
							print(app.stopped_playing_sound)
							app.played_sounds.append([self,root.source[root.index]]) if [self,root.source[root.index]] not in app.played_sounds else app.passs()
							self.icon = 'play' if app.playing_sound and app.playing_sound_source == root.source[root.index] and app.playing_sound.state== 'stop' else('pause' if app.playing_sound and app.playing_sound_source == root.source[root.index] else 'play')
					IconButton:
						pos_hint:{'center_y':.5}
						size_hint:None,None
						size:dp(45),dp(45)
						halign: 'center'
						valign:'middle'
						theme_text_color: 'Custom'
						disabled: False if self.icon == 'skip-next-circle-outline' else True
						text_color:[.9,.7,.225,.9] if self.icon == 'skip-next-outline' else [1,.75,.25,1]
						icon: 'skip-next-outline' if root.index>=(len(root.audio)-1) else 'skip-next-circle-outline'
						font_size:dp(45)
						on_release:
							app.stopped_playing_sound = None
							app.pause_audio()
							root.index = root.index if root.index>=(len(root.audio)-1) else root.index+1
							app.play_audio(root.source[root.index])
							app.played_sounds.append([play_button,root.source[root.index]]) if [play_button,root.source[root.index]] not in app.played_sounds else app.passs()
							play_button.icon = 'play' if app.playing_sound and app.playing_sound_source == root.source[root.index] and app.playing_sound.state== 'stop' else('pause' if app.playing_sound and app.playing_sound_source == root.source[root.index] else 'play')
				Widget:
					size_hint_x:None
					width:(app.window.width/2)-dp(75+100)
				MDRoundFlatIconButton:
					icon: 'pin' if root.pinned[root.index] else ('pin' if root.audio[root.index][1] in app.live_pinned_users else ('pin-off' if root.audio[root.index][1] in app.live_unpinned_users else 'pin-off'))
					text: 'Pin' if self.icon == 'pin-off' else 'Pinned'
					size_hint: None,None
					markup: True
					height:dp(35)
					disabled: False if root.audio[root.index][1] != app.user else True
					opacity:0 if self.disabled else 1
					width: dp(80) if self.text == 'Pin' else dp(100)
					md_bg_color: [0.0, 0.0, 0.0, 0.0] if self.icon == 'pin-off' else [1,.75,.25,.75]
					pos_hint: {'center_y':.5,'center_x':.5}
					theme_text_color: 'Custom'
					text_color: [.1,.1,.1,1] if self.icon == 'pin-off' else [.75,0,1,1]
					on_press:
						app.pin_user(root.audio[root.index][1],root)
				
<SearchScreen>
	name: 'search_screen'
	id: search_screen
	on_enter: search_tabs.opacity = 1
	on_leave: search_tabs.opacity = 0
	BoxLayout:
		orientation:'vertical'
		size_hint_y: 1
		spacing: dp(0)
		MDCard:
			size_hint:1,.1
			pos_hint: {'top':1}
			spacing: dp(10)
			padding:dp(10)
			canvas:
				Color:
					rgba:[.975,.975,.975,1]
				Rectangle:
					pos:self.pos
					size:self.size
			MDIconButton:
				icon:'arrow-left'
				pos_hint: {'center_y':.5}
				on_press:
					search_tabs.opacity = 0
					root.manager.transition.direction = 'right'
					root.manager.remove_widget(root)
			SearchTextInput:
				multiline: False
				size_hint: 1,1
				hint_text:'Search on Pulsar ...' if search_tabs.carousel.index == 0 else('Search people ...' if search_tabs.carousel.index == 1 else 'Search hashtags ...')
				on_text: 
					app.my_galaxy_search(self,search_result_list)
				border: [0,0,0,0]
    			selection_color: [.7,.3,.05,.4]
				background_color: [0,0,0,0]
			MDIconButton:
				icon:'magnify'
				pos_hint: {'center_y':.5}
		MDTabs:
			id: search_tabs
			background_color: [.975,.975,.975,1]
			text_color_normal: [0,0,0,1]
			text_color_active:[.5,0,1,1]
			opacity:0
			TabsBase:
				text: 'format-list-bulleted'
				ScrollView:
					size_hint:1,1
					effect_cls: 'ScrollEffect'
					BoxLayout:
						id:search_result_list
						orientation: 'vertical'
						size_hint: 1,None
						padding: dp(0)
						spacing: dp(5)
						height: self.minimum_height
						
									
			TabsBase:
				text: 'account'
			TabsBase:
				text: 'music-accidental-sharp'

<SearchCard>
	spacing:dp(5)
	size_hint: 1,None
	padding:dp(10)
	height: dp(65)
	Widget:
		size_hint_x:.025
	RoundImageTouch:
		size_hint:None,.95
		pos_hint: {'center_y':.5}
		width:self.height
		source:root.info[3] if root.info[3]!= '' else app.avatar
	BoxLayout:
		size_hint:1,1
		orientation:'vertical'
		MDLabel:
	        text: '@'+root.info[1]
	        theme_text_color: 'Custom'
	        halign: 'left'
	        text_color:[0,0,0,1]
        	font_size: dp(18)
	        shorten: True
	        shorten_from: 'right'
	    MDLabel:
	    	text: root.info[2] if root.info[2]!='' else root.info[4]
	    	font_size: dp(15)
	    	theme_text_color: 'Custom'
	        halign: 'left'
	        text_color:[0,0,0,.75]
	        shorten: True
	        shorten_from: 'right'
<NotificationScreen>
	name: 'notifications_screen'
	icon: 'bell'
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			pos:self.pos
			size: self.size
	ScreenManager:
		id: screen_manager
		Screen:
			id: main
			name: 'main'
			BoxLayout:
				orientation: "vertical"
				spacing: dp(5)
				size_hint_y: 1
				id: notification_layout
				MDTabs:
					id: tab_try
					background_color: [1,.98,.955,1]
					text_color_normal: [0,0,0,1]
					text_color_active:[.5,0,1,1]
					TabsBase:
						text: 'Personal'
						ScrollView:
							size_hint:1,1
							effect_cls: 'ScrollEffect'
							BoxLayout:
								orientation: 'vertical'
								size_hint: 1,None
								padding: dp(10)
								spacing: dp(15)
								height: self.minimum_height
								PinCard:
								LikedCard:
								PinCard:
								LikedCard:
								PinCard:
								LikedCard:
								PinCard:
								LikedCard:
								PinCard:
								LikedCard:

									
					TabsBase:
						text: 'Tags'
<PinCard>
	orientation: 'horizontal'
	spacing: dp(10)
	size_hint: 1,None
	height: dp(50)
	RoundImageTouch:
		elevation:0
		source: 'assets/andre-rodriges.png'
		size_hint:None,None
		size: dp(50),dp(50)
		pos_hint:{'center_y':.5}
	BoxLayout:
		orientation: 'vertical'
		size_hint:1,1
		BoxLayout:
			size_hint:1,1
			spacing: dp(10)
			MDTextButton:
				text: 'Username'
				bold: True
				custom_color: [0,0,0,1]
				size_hint_x:None
				pos_hint:{'center_y':.5}
			Widget:
			MDLabel:
				text: 'Time'
				font_size: dp(12)
				size_hint_x:None
				size_hint_y:.5
				pos_hint:{'right':1,'center_y':.5}
		MDLabel:
			text: 'Has pinned you.'
	PinIcon:
		pos_hint:{'center_y':.5}

<LikedCard>
	orientation: 'horizontal'
	spacing: dp(10)
	size_hint: 1,None
	height: dp(50)
	RoundImageTouch:
		elevation:0
		source: 'assets/heattheatr.png'
		size_hint:None,None
		size: dp(50),dp(50)
		pos_hint:{'center_y':.5}
	BoxLayout:
		orientation: 'vertical'
		size_hint:1,1
		BoxLayout:
			size_hint:1,1
			spacing: dp(10)
			MDTextButton:
				text: 'Username'
				bold: True
				custom_color: [0,0,0,1]
				size_hint_x:None
				pos_hint:{'center_y':.5}
			Widget:
			MDLabel:
				text: 'Time'
				font_size: dp(12)
				size_hint_x:None
				size_hint_y:.5
				pos_hint:{'right':1,'center_y':.5}
		MDLabel:
			text: 'Likes your post.'
	ImageTouch:
		source: 'assets/images (22).jpg'
		size_hint: None,1
		width:self.height*self.image_ratio


<PostScreen>
	name: 'post_screen'
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			pos:self.pos
			size: self.size
	BoxLayout:
		size_hint: 1,1
		orientation: 'vertical'
		spacing: dp(0)
		id: postscreen_layout
		MDCard:
			size_hint: 1,.1
			pos_hint:{'top':1}
			canvas:
				Color:
		    		rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
				    size: self.size
			        pos: self.pos
			MDIconButton:
				icon: 'arrow-left'
				pos_hint: {'center_y':.5}
				size_hint: None,None
				on_press:
					app.video_cache()
					app.root_manager.current = 'basic_root'
					app.root_manager.transition = sm.SlideTransition()
					
			Widget:
			MDTextButton:
		    	text: 'Post'
		    	custom_color: [.75,0,1,1]
		    	font_size: dp(18)
		    	pos_hint: {'center_y':.5}
		    	on_press: app.upload_post(root.upload_mode,caption.text,emotion.text)
		    Widget:
				size_hint_x: None
				width: dp(10)

		ScrollView:
			size_hint:1,1
			effect_cls: 'ScrollEffect'
			canvas.before:
				Color:
		    		rgba: [1,1,1,1]
			    Rectangle:
				    size: self.size
			        pos: self.pos
			BoxLayout:
				id: posting_layout
				size_hint: 1,None
				orientation: 'vertical'
				height:self.minimum_height
				padding: dp(10)
				spacing: dp(10)
				BoxLayout:
					size_hint: None,None
					width:self.minimum_width
					pos_hint:{'center_x':.5}
					height: self.minimum_height
					spacing: app.window.width/15
					MDIconButton:
						icon: 'camera'
						size_hint:None,None
						height:app.window.width/7.5
						width:self.height
						pos_hint:{'center_y':.5}
						user_font_size: self.height/1.5
						theme_text_color:'Custom'
						text_color: [.1,0,.2,1]
						on_press: 
							app.open_gallery_images()
					MDIconButton:
						icon: 'video'
						size_hint:None,None
						height:app.window.width/7.5
						width:self.height
						pos_hint:{'center_y':.5}
						user_font_size: self.height/1.5
						theme_text_color:'Custom'
						text_color: [.1,0,.2,1]
						on_press: 
							app.open_gallery_video()
					MDIconButton:
						icon: 'music'
						size_hint:None,None
						height:app.window.width/7.5
						width:self.height
						pos_hint:{'center_y':.5}
						user_font_size: self.height/1.5
						theme_text_color:'Custom'
						text_color: [.1,0,.2,1]
						on_press:
							app.open_gallery_audio()
				FullSeparator:
				BoxLayout:
					size_hint: 1, None
					height: dp(100)
					padding: dp(10)
					RoundImageTouch: 
						id: profile_pic
						size_hint: None,None
						size: dp(75),dp(75)
						pos_hint: {'top':1,'center_y': .5}
						on_release: caption.focus = True
					TextInput:
						id: caption
						size_hint:.8,None
						hint_text: 'Add a caption ...'
				    	border: [0,0,0,0]
				    	height: self.minimum_height if self.minimum_height<dp(100) else dp(100)
				    	selection_color: [.7,.3,.05,.4]
				    	background_color: [0,0,0,0]
				    	pos_hint: {'center_y':.5}
				BoxLayout:
					id: em_lay
					orientation: 'vertical'
					size_hint: 1,None
					height: self.minimum_height
					BoxLayout:
						size_hint: 1, None
						height: dp(50)
						spacing: dp(5)
						padding: dp(0)
						MDIcon: 
							size_hint: None,None
							size: dp(50),dp(50)
							font_size:dp(40)
							icon:'emoticon-poop'
							pos_hint: {'center_y': .5}
						MDTextField:
							id: emotion
							scroll_x:1
							hint_text:'Emotion/Slogan'
				
				
				BoxLayout:
					id: tags_lay
					orientation: 'vertical'
					size_hint: 1,None
					height: self.minimum_height
					BoxLayout:
						size_hint: 1, None
						height: dp(50)
						spacing: dp(5)
						padding: dp(0)
						MDIcon: 
							size_hint: None,None
							size: dp(50),dp(50)
							font_size:dp(40)
							icon:'music-accidental-sharp'
							pos_hint: {'center_y': .5}
						TagsTextInput:
							layout: chosen_tags_lay
							id: tags
							on_text_validate: self.focus = True
							hint_text: 'Tagname'
					StackLayout:
						id: chosen_tags_lay
						size_hint:1,None
						spacing:dp(5)
						height:self.minimum_height

				PostScreenPostingLayout:
					id:posting_media_layout
					orientation: 'vertical'
					size_hint:1,None
					height:self.minimum_height
<ChosenTagsCard>
	size_hint:None,None
	height:dp(30)
	padding:dp(2.5)
	width:self.minimum_width
	canvas:
		Color:
			rgba: [.1,.1,.1,.075]
		RoundedRectangle
			size: self.size
			pos: self.pos
			radius:[10]
	MDTextButton:
		text:root.text
		custom_color:[.3,.1,1,1]
		font_size:dp(15)
		pos_hint:{'center_y':.5}
	IconButton:
		icon:'close'
		size_hint:None,None
		size:dp(25),dp(25)
		halign:'right'
		valign:'top'
		font_size:dp(15)
		on_release:app.remove_tag(root)
<PostScreenImageLayout>
	id: post_layout
	size_hint: 1,None
	cols: 3
	height: self.minimum_height
	spacing: dp(5)
<PostScreenAudioLayout>
	id: audio_layout
	size_hint: .8,None
	pos_hint:{'center_x':.5}
	orientation: 'vertical'
	height: self.minimum_height
<PostScreenVideoLayout>
	id: video_layout
	size_hint: 1,None
	padding:dp(0)
	height: self.minimum_height
<CameraScreen>


<GalleryImages>
	size_hint: 1, 1
	pos_hint: {'center_y':.5}
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			size: self.size
			pos: self.pos
	BoxLayout:
		orientation:'vertical'
		size_hint: 1, 1
		pos_hint: {'center_x':.5,'center_y':.5}
		MDCard:
			size_hint: 1,.1
			padding: 3
			spacing: dp(5)
			canvas:
		    	Color:
			    	rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
			        size: self.size
		            pos: self.pos
		    MDIconButton:
		    	icon: 'arrow-left'
		    	on_press: 
		    		root.dismiss() if len(app.posting_register)==0 else app.gallery_images_dialog(root)
		    	pos_hint: {'center_y':.5}
		    MDLabel:
		    	text: "Gallery Images"
		    	font_size: dp(18)
		    NotificationCount:
		    	id: post_count
		    	pos_hint: {'center_y':.5}
		    	size: dp(30),dp(30)
		    	count: str(len(app.posting_register))
		    Widget:
		    	size_hint_x:None
		    	width: dp(10)
		    MDIconButton:
		    	id: post_check
		    	p_c: 0
		    	icon: 'check' if self.p_c<2 else 'check-all'
		    	theme_text_color: 'Custom'
		    	text_color: [0,0,0,.5] if self.p_c<1 else [.5,0,1,1]
		    	on_press: 
		    		root.dismiss()
		    		app.display_selected_posts()
		    	pos_hint: {'center_y':.5}
		ScrollView:
			size_hint: 1,.9
			effect_cls: 'ScrollEffect'
			GridLayout:
				id: gallery_scroll
				cols: 3
				padding: dp(1)
		        spacing: dp(3)
		        size_hint_y: None
		        height: self.minimum_height
		        BoxLayout:
		        	size_hint:1,1
			        ImageTouch:
			        	size_hint:None,.8
			        	width:self.height*self.image_ratio
			        	source:"assets/camera_icon.png"
			        	pos_hint:{'center_y':.5,'center_x':.5}
			        	on_press:
			        		app.open_camera()
<GalleryAudio>
	size_hint: 1, 1
	pos_hint: {'center_y':.5}
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			size: self.size
			pos: self.pos
	BoxLayout:
		orientation:'vertical'
		size_hint: 1, 1
		pos_hint: {'center_x':.5,'center_y':.5}
		MDCard:
			size_hint: 1,.1
			padding: 3
			spacing: dp(5)
			canvas:
		    	Color:
			    	rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
			        size: self.size
		            pos: self.pos
		    MDIconButton:
		    	icon: 'arrow-left'
		    	on_press: 
		    		root.dismiss()
		    		app.preview_audio.stop() if app.preview_audio else app.passs()
		    		app.preview_audio_pause(None)
		    		app.preview_audio = None
		    		app.preview_audio_cache()
		    	pos_hint: {'center_y':.5}
		    MDLabel:
		    	text: "Gallery Audio"
		    	font_size: dp(18)
		ScrollView:
			size_hint: 1,.9
			effect_cls: 'ScrollEffect'
			GridLayout:
				id: gallery_scroll
				cols: 1
				padding: dp(5)
		        spacing: dp(5)
		        size_hint_y: None
		        height: self.minimum_height
<GalleryAudioLayout>
	size_hint:1,None
	height: dp(50)
	spacing: dp(5)
	on_press: app.select_audio_post(root.source)
	MDIconButton:
		icon: 'music'
		pos_hint: {'center_y':.5}
		size_hint: None,1
		user_font_size: dp(30)
		width: self.height
	BoxLayout:
		id: info
		orientation: 'vertical'
		size_hint: None,1
		pos_hint: {'right':1}
		width: root.width-(dp(110))
		MDLabel:
			text: root.name
			font_size: dp(15)
			size_hint_x:1
			shorten: True
			shorten_from: 'right'
			pos_hint: {'center_y':.5}
			halign: 'left'
		BoxLayout:
			size_hint_x:1
			MDLabel:
				halign: 'left'
				text: root.duration
				shorten: True
				font_size: dp(12)
				shorten_from: 'right'
				pos_hint: {'left':1}
				theme_text_color: 'Custom'
				text_color: [0,0,0,.75]
			Widget:
			MDLabel:
				text: root.filesize+' mb'
				shorten: True
				font_size: dp(12)
				halign: 'right'
				shorten_from: 'right'
				pos_hint: {'right':1}
				theme_text_color: 'Custom'
				text_color: [0,0,0,.75]
	MDIconButton:
		size_hint: None,None
		user_font_size: dp(20)
		pos_hint: {'center_y':.5}
		icon: 'play' if app.preview_audio and app.preview_audio_source == root.source and app.preview_audio.state== 'stop' else('pause' if app.preview_audio and app.preview_audio_source == root.source else 'play')
		on_press: 
			app.preview_audio_play(root.source) if self.icon == 'play' else app.preview_audio_pause(root.source)
			app.played_preview_audio.append([self,root.source]) if [self,root.source] not in app.played_preview_audio else app.passs()
			self.icon = 'play' if app.preview_audio and app.preview_audio_source == root.source and app.preview_audio.state == 'stop' else('pause' if app.preview_audio and app.preview_audio_source == root.source else 'play')
<AudioCoverImageSelect>
	FitImageTouch:
		id: cover_image
		size_hint: 1,1
		pos_hint: {'center_x':.5}
		source: root.source
	MDIconButton:
		id: choose_cover_image
		user_font_size: self.parent.height/5
		icon: 'assets/account-camera.png'
		pos_hint: {'center_x':.95,'center_y':0.05}
		on_press: app. open_cover_image_select(root.parent)
<PostingAudioLayout>
	orientation: 'vertical'
	size_hint:1,None
	height: self.minimum_height +dp(10)
	pos_hint: {'center_x':.5}
	spacing:dp(5)
	padding: [10,0,10,10]
	BoxLayout:
		id: cover_lay
		size_hint:.75,None
		height:self.width
		pos_hint: {'center_x':.5}
		AudioCoverImageSelect:
			id: cv_image
	Widget:
		size_hint_y: None
		height: dp(15)
	MDLabel:
		id: user
		text: app.user_info[2]
		theme_text_color: 'Custom'
		text_color: [0,0,0,.75]
		halign: 'center'
	Widget:
		size_hint_y: None
		height: dp(20)
	MDLabel:
		text: 'Title'
		font_size: dp(12)
		theme_text_color: 'Custom'
		text_color: [0,0,0,.75]
		halign: 'left'
	MDTextField:
		id: title
		scroll_x:1
		text: root.filename

<GalleryVideo>
	size_hint: 1, 1
	pos_hint: {'center_y':.5}
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			size: self.size
			pos: self.pos
	BoxLayout:
		orientation:'vertical'
		size_hint: 1, 1
		pos_hint: {'center_x':.5,'center_y':.5}
		MDCard:
			size_hint: 1,.1
			padding: 3
			spacing: dp(5)
			canvas:
		    	Color:
			    	rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
			        size: self.size
		            pos: self.pos
		    MDIconButton:
		    	icon: 'arrow-left'
		    	on_press: 
		    		root.dismiss()
		    	pos_hint: {'center_y':.5}
		    MDLabel:
		    	text: "Gallery Video"
		    	font_size: dp(18)
		ScrollView:
			size_hint: 1,.9
			effect_cls: 'ScrollEffect'
			GridLayout:
				id: gallery_scroll
				cols: 3
				padding: dp(5)
		        spacing: dp(5)
		        size_hint_y: None
		        height: self.minimum_height
<GalleryImagesSingle>
	size_hint: 1, 1
	pos_hint: {'center_y':.5}
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			size: self.size
			pos: self.pos
	BoxLayout:
		orientation:'vertical'
		size_hint: 1, 1
		pos_hint: {'center_x':.5,'center_y':.5}
		MDCard:
			size_hint: 1,.1
			padding: 3
			spacing: dp(5)
			canvas:
		    	Color:
			    	rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
			        size: self.size
		            pos: self.pos
		    MDIconButton:
		    	icon: 'arrow-left'
		    	on_press: 
		    		root.dismiss()
		    	pos_hint: {'center_y':.5}
		    MDLabel:
		    	text: "Gallery Images"
		    	font_size: dp(18)
		ScrollView:
			size_hint: 1,.9
			effect_cls: 'ScrollEffect'
			GridLayout:
				id: gallery_scroll
				cols: 3
				padding: dp(1)
		        spacing: dp(3)
		        size_hint_y: None
		        height: self.minimum_height

<EditPostScreen>
	name: 'post_screen'
	canvas:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			pos:self.pos
			size: self.size
	BoxLayout:
		size_hint: 1,1
		orientation: 'vertical'
		spacing: dp(0)
		id: postscreen_layout
		MDCard:
			size_hint: 1,.1
			pos_hint:{'top':1}
			canvas:
				Color:
		    		rgba: [1,1,1,.025]
			    Rectangle:
			    	source: 'assets/toolbar.png'
				    size: self.size
			        pos: self.pos
			MDIconButton:
				icon: 'arrow-left'
				pos_hint: {'center_y':.5}
				size_hint: None,None
				on_press:
					#app.video_cache()
					#app.root_manager.current = 'basic_root'
					#app.root_manager.transition = sm.SlideTransition()
					
			Widget:
			MDTextButton:
		    	text: 'Update'
		    	custom_color: [.75,0,1,1]
		    	font_size: dp(18)
		    	pos_hint: {'center_y':.5}
		    	on_press: app.update_post(caption.text,emotion.text)
		    Widget:
				size_hint_x: None
				width: dp(10)

		ScrollView:
			size_hint:1,1
			effect_cls: 'ScrollEffect'
			canvas.before:
				Color:
		    		rgba: [1,1,1,1]
			    Rectangle:
				    size: self.size
			        pos: self.pos
			BoxLayout:
				id: posting_layout
				size_hint: 1,None
				orientation: 'vertical'
				height:self.minimum_height
				padding: dp(10)
				spacing: dp(10)
				BoxLayout:
					size_hint: 1, None
					height: dp(100)
					padding: dp(10)
					RoundImageTouch: 
						id: profile_pic
						size_hint: None,None
						size: dp(75),dp(75)
						pos_hint: {'top':1,'center_y': .5}
						on_release: caption.focus = True
					TextInput:
						id: caption
						size_hint:.8,None
						hint_text: 'Add a caption ...'
				    	border: [0,0,0,0]
				    	height: self.minimum_height if self.minimum_height<dp(100) else dp(100)
				    	selection_color: [.7,.3,.05,.4]
				    	background_color: [0,0,0,0]
				    	pos_hint: {'center_y':.5}
				BoxLayout:
					id: em_lay
					orientation: 'vertical'
					size_hint: 1,None
					height: self.minimum_height
					BoxLayout:
						size_hint: 1, None
						height: dp(50)
						spacing: dp(5)
						padding: dp(0)
						MDIcon: 
							size_hint: None,None
							size: dp(50),dp(50)
							font_size:dp(40)
							icon:'emoticon-poop'
							pos_hint: {'center_y': .5}
						MDTextField:
							id: emotion
							scroll_x:1
							hint_text:'Emotion/Slogan'
				
				
				BoxLayout:
					id: tags_lay
					orientation: 'vertical'
					size_hint: 1,None
					height: self.minimum_height
					BoxLayout:
						size_hint: 1, None
						height: dp(50)
						spacing: dp(5)
						padding: dp(0)
						MDIcon: 
							size_hint: None,None
							size: dp(50),dp(50)
							font_size:dp(40)
							icon:'music-accidental-sharp'
							pos_hint: {'center_y': .5}
						TagsTextInput:
							layout: chosen_tags_lay
							id: tags
							on_text_validate: self.focus = True
							hint_text: 'Tagname'
					StackLayout:
						id: chosen_tags_lay
						size_hint:1,None
						spacing:dp(5)
						height:self.minimum_height

				PostScreenPostingLayout:
					id:posting_media_layout
					orientation: 'vertical'
					size_hint:1,None
					height:self.minimum_height

<TagScreen>
	name: 'tag_screen'
	BoxLayout:
		size_hint: 1,1
		orientation: 'vertical'
		spacing: dp(0)
		RelativeLayout:
			size_hint:1,1
			ScrollView:
				size_hint:1,1
				id: tag_scroll
				do_scroll:(False,True)
				effect_cls: 'ScrollEffect'
				BoxLayout:
					id: main_box
					orientation: 'vertical'
					size_hint: 1,None
					height: self.minimum_height
					padding: dp(0)
					spacing: dp(0)
					RelativeLayout:
						size_hint:1,None
						height: cover_image.height + (app.window.width/4)
						pos_hint: {'center_x':.5}
						FitImageTouch:
							id: cover_image
							allow_stretch: True
							pos_hint: {'top':1}
							source: root.tag_cover_pic
							size_hint: 1,None
							height: self.width/1.5
						RelativeLayout:
							size_hint:.5,None
							height:self.width
							pos_hint: {'center_x':.5,'bottom':1}
							RoundImageTouch:
								size_hint: 1,1
								source: 'assets/andre-rodriges.png'
							IconButton:
								size_hint:.25,.25
								font_size:self.parent.height*0.25
								icon:'plus-circle'
								pos_hint:{'right':1,'bottom':1}
								theme_text_color: 'Custom'
								text_color:[.75,0,1,1] if self.icon == 'plus-circle' else [1,.75,.25,1]
								on_press:
									self.icon = 'check-circle' if self.icon=='plus-circle' else 'plus-circle'
					BoxLayout:
						size_hint: None,None
						pos_hint: {'center_x':.5}
						width: self.minimum_width
						height: dp(70)
						spacing: dp(10)
						BoxLayout:
							orientation: 'vertical'
							size_hint:None,1
							width: dp(75)
							MDLabel:
								bold: True
								text: str(root.post_count) if root.post_count>=0 else '-'
								halign: 'center'
							MDLabel:
								text: 'Post' if root.post_count==1 else 'Posts'
								shorten: True
								shorten_from: 'right'
								halign: 'center'
						MDSeparator:
							orientation: 'vertical'
						BoxLayout:
							orientation: 'vertical'
							size_hint:None,1
							width: dp(75)
							MDLabel:
								bold: True
								text: '2.04 K'
								halign: 'center'
							MDLabel:
								text: 'Pins'
								shorten: True
								shorten_from: 'right'
								halign: 'center'
						MDSeparator:
							orientation: 'vertical'
						BoxLayout:
							orientation: 'vertical'
							size_hint:None,1
							width: dp(75)
							MDLabel:
								bold: True
								text: '4.7'
								halign: 'center'
							MDLabel:
								text: 'Rating'
								shorten: True
								shorten_from: 'right'
								halign: 'center'
					FullSeparator:
					MyTabs:
						ButtonBoxLayoutPlain:
							MDTextButton:
								id: recent_tab
								size_hint: .5,1
								text: 'Recent'
								halign: 'center'
								font_size: dp(20)
								shorten: True
								shorten_from: 'right'
								bold: True if scrn_manager.current == 'tecent_screen' else False
								custom_color: [.25,0,.5,1] if scrn_manager.current == 'recent_screen' else [0,0,0,1]
								pos_hint: {'center_y':.5}
								on_press:
									a = scrn_manager.height if scrn_manager.height>=app.window.height*0.81 else app.window.height*0.81
									scrn_manager.transition.direction = 'right'
									scrn_manager.current = 'recent_screen'
									recent_height = recent_screen.height if recent_screen.height> app.window.height*0.81 else app.window.height*0.81
									scrn_manager.height = recent_height
									layout.height = recent_height
									app.adjust_scroll_special([main_box,recent_height-a])
					    ButtonBoxLayoutPlain:
							MDTextButton:
								id: trending_tab
								size_hint: .5,1
								text: 'Trending'
								halign: 'center'
								font_size: dp(20)
								shorten: True
								shorten_from: 'right'
								bold: True if scrn_manager.current == 'trending_screen' else False
								custom_color: [.25,0,.5,1] if scrn_manager.current == 'trending_screen' else [0,0,0,1]
								pos_hint: {'center_y':.5}
								on_press:
									a = scrn_manager.height if scrn_manager.height>=app.window.height*0.81 else app.window.height*0.81
									scrn_manager.transition.direction = 'left'
									scrn_manager.current = 'trending_screen'
									trending_height = trending_screen.height if trending_screen.height> app.window.height*0.81 else app.window.height*0.81
									scrn_manager.height = trending_height
									layout.height = trending_height
									app.adjust_scroll_special([main_box,trending_height-a])
					FullSeparator:
					BoxLayout:
						id: layout
						size_hint: 1, None
						pos_hint:{'top':1}
						height: self.minimum_height if self.minimum_height> app.window.height*0.81 else app.window.height*0.81
						ScreenManager:
							id: scrn_manager
							size_hint:1,None
							height: recent_screen.height
							pos_hint:{'top':1}
							Screen:
								id: recent_screen
								name: 'recent_screen'
								size_hint:1,None
								height:recent_layout.height
								pos_hint:{'top':1}
								on_enter:
								GridLayout:
									id: recent_layout
									size_hint:1,None
									pos_hint:{'top':1}
									cols: 3
									spacing: dp(1.2)
									height: self.minimum_height
							Screen:
								id: trending_screen
								name: 'trending_screen'
								size_hint:1,None
								height:trending_layout.height
								pos_hint:{'top':1}
								on_enter:root.trending_enter()
								GridLayout:
									id: trending_layout
									size_hint_x:1
									pos_hint:{'top':1}
									cols: 3
									spacing: dp(1.2)
									height: self.minimum_height
			BoxLayout:
				orientation:"horizontal"
				size_hint_y: .1
				pos_hint:{'top':1}
				padding: dp(0)
				list: 
				spacing: dp(5)
				canvas.before:
			    	Color:
					    rgba: [1,1,1,(0.75*(1-tag_scroll.scroll_y)*main_box.height)/(app.window.width/1.5)] if ((1-tag_scroll.scroll_y)*main_box.height)<(app.window.width) else [1,1,1,1]
				    Rectangle:
					    size: self.size
				        pos: self.pos
				canvas:
			    	Color:
					    rgba: [1,1,1,(0.025*(1-tag_scroll.scroll_y)*main_box.height)/(app.window.width/1.5)] if ((1-tag_scroll.scroll_y)*main_box.height)<(app.window.width) else [1,1,1,0.025]
				    Rectangle:
				    	source: 'assets/toolbar.png'
					    size: self.size
				        pos: self.pos
				MDIconButton:
			    	icon: 'arrow-left'
			    	pos_hint: {'center_y':.5}
			    	custom_color: [1,0,0,1]
					on_press: 
						app.close_screen(root)
				Widget:
					size_hint_x:None
					width:dp(10)
			    MDLabel:
			    	text: root.tag_name
			    	font_size: dp(20)
			    	shorten: True
					shorten_from: 'right'
					size_hint_x:1
				MDIconButton:
					icon: "star-outline"
					pos_hint:{"center_y": .5}
					theme_text_color:'Custom'
					text_color:[1,.75,.25,.75] if self.icon =='star' else [0,0,0,1]
					on_press:
						self.icon = 'star' if self.icon == 'star-outline' else 'star-outline'
				Widget:
					size_hint_x:None
					width:dp(5)

<RoundImageTouch>
	canvas:
		Color:
			rgba: [1,1,1,1]
		Ellipse:
			pos:self.pos
			source: root.source
			size: self.size
<RoundImage>
	canvas:
		Color:
			rgba: [1,1,1,1]
		Ellipse:
			pos:self.pos
			source: root.source
			size: self.size
<FitImageTouch>
	canvas.before:
		Color:
			rgba: [0,0,0,.05]
		Rectangle:
			pos: self.pos
			size: self.width+dp(1),self.height+dp(1)
	canvas.after:
		Color:
			rgba: [1,1,1,0]
		Rectangle:
			pos:self.pos
			size:self.size
<GalleryFitImageTouch>
	canvas.before:
		Color:
			rgba: [0,0,0,.05]
		Rectangle:
			pos: self.pos
			size: self.width+dp(1),self.height+dp(1)
	canvas.after:
		Color:
			rgba: [1,1,1,0] if root.selected ==False else [.7,0,1,.2]
		Rectangle:
			pos:self.pos
			size:self.size
	RelativeLayout:
		size_hint: 1,1
		FitImage:
			size_hint: 1,1
			source: root.source
		RelativeLayout:
			size_hint:None,None
			size: root.width/4,root.width/4
			pos_hint: {'right':1,'top':1}
			MDIcon:
				icon: 'circle-outline' if root.selected == False else 'circle'
				size_hint: 1,1
				user_font_size: dp(20)
				theme_text_color: 'Custom'
				text_color: [1,1,1,.75] if root.selected == False else [0,1,0,1]
<FitMultipleImageTouch>
	canvas.before:
		Color:
			rgba: [0,0,0,.05]
		Rectangle:
			pos: self.pos
			size: self.width+dp(1),self.height+dp(1)
	canvas.after:
		Color:
			rgba: [1,1,1,0]
		Rectangle:
			pos:self.pos
			size:self.size
	RelativeLayout:
		size_hint: 1,1
		FitImage:
			size_hint: 1,1
			source: root.source
		MDIcon:
			icon: 'image-multiple'
			size_hint: None,None
			size: root.width/4,root.width/4
			pos_hint: {'right':1,'top':1}
			theme_text_color: 'Custom'
			text_color: [1,1,1,.9]
<FitAudioTouch>
	canvas.before:
		Color:
			rgba: [0,0,0,.05]
		Rectangle:
			pos: self.pos
			size: self.width+dp(1),self.height+dp(1)
	canvas.after:
		Color:
			rgba: [1,1,1,0] if root.selected ==False else [.7,0,1,.5]
		Rectangle:
			pos:self.pos
			size:self.size
	RelativeLayout:
		size_hint: 1,1
		FitImage:
			size_hint: 1,1
			source: root.source
		MDIcon:
			icon: 'headphones-box'
			size_hint: None,None
			size: root.width/3,root.width/3
			font_size: self.width*0.75
			pos_hint: {'right':1,'top':1}
			theme_text_color: 'Custom'
			text_color: [1,1,1,.9]
<FitVideoTouch>
	canvas.before:
		Color:
			rgba: [0,0,0,.05]
		Rectangle:
			pos: self.pos
			size: self.width+dp(1),self.height+dp(1)
	canvas.after:
		Color:
			rgba: [1,1,1,0] if root.selected ==False else [.7,0,1,.5]
		Rectangle:
			pos:self.pos
			size:self.size
	RelativeLayout:
		size_hint: 1,1
		FitImage:
			size_hint: 1,1
			source: root.source
		MDIcon:
			icon: 'video-vintage'
			size_hint: None,None
			size: root.width/3,root.width/3
			font_size: self.width*0.75
			pos_hint: {'right':1,'top':1}
			theme_text_color: 'Custom'
			text_color: [1,1,1,.9]
<ImageTouch>
	canvas.before:
		Color:
			rgba: [1,1,1,1]
		Rectangle:
			pos:self.pos
			size: self.size
<ImageBGEXT>
	canvas:
		Color:
			rgba: [1,1,1,.95]
		Rectangle:
			pos: self.pos
			source:self.source
			size: self.size
<NotificationCount>
	size_hint: None,None
	canvas:
		Color:
			rgba:[.75,0,1,1]
		Ellipse:
			pos:self.pos
			size: self.size
	Label:
		text: root.count
		bold: True
		pos_hint: {'center_y':.5}
		valign: 'center'
		halign: 'center'
<WarningPopup>
	size_hint:.8,None
	auto_dismiss: True
	background_color:[0,0,0,.1]
	pos_hint: {'center_x':.5,'center_y':.5}
	height: lay.height
	canvas:
		Color:
			rgba: [1,1,1,1]
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius:[20]
	BoxLayout:
		id:lay
		orientation: 'vertical'
		size_hint:1,None
		height:self.minimum_height
		padding:dp(10)
		Widget:
			size_hint_y:None
			height:dp(10)
		
		MDLabel:
			size_hint:1,None
			height:dp(20)
			font_size:dp(20)
			theme_text_color:'Custom'
			text_color:[.1,0,.2,1]
			halign: 'center'
			text:'Warning'
		BoxLayout:
			size_hint:1,None
			height:self.minimum_height
			MDLabel:
				id: label
				text: root.message
				text_size:(root.width), None
				size_hint_y:None
				height: (self._label.render())[1]
				theme_text_color:'Custom'
				text_color:[0,0,0,.75]
				halign:'center'
				valign: 'middle'
		BoxLayout:
			size_hint:1,None
			height:dp(20)
			spacing: dp(10)
			padding:dp(10)
			MDTextButton:
				text:'Cancel'
				font_size:dp(18)
				halign:'left'
				pos_hint:{'center_y':.5}
				custom_color:[0,0,0,.5]
				on_release: 
					root.callback(self.text)
					root.dismiss()
			Widget:
			MDTextButton:
				text:'Ok'
				font_size:dp(20)
				halign:'right'
				custom_color:[.1,0,.2,1]
				pos_hint:{'center_y':.5}
				on_release: 
					root.callback(self.text)
					root.dismiss()
<ConfirmationPopup>
	size_hint:.8,None
	auto_dismiss: True
	background_color:[0,0,0,.1]
	pos_hint: {'center_x':.5,'center_y':.5}
	height: lay.height
	canvas:
		Color:
			rgba: [1,1,1,1]
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius:[20]
	BoxLayout:
		id:lay
		orientation: 'vertical'
		size_hint:1,None
		height:self.minimum_height
		padding:dp(10)
		spacing:dp(0)
		Widget:
			size_hint_y:None
			height:dp(10)
		MDLabel:
			size_hint:1,None
			height:dp(20)
			font_size:dp(20)
			theme_text_color:'Custom'
			text_color:[.1,0,.2,1]
			halign: 'center'
			text:'Confirmation'
		BoxLayout:
			size_hint:1,None
			height:self.minimum_height
			MDLabel:
				id: label
				text: root.message
				text_size:(root.width), None
				size_hint_y:None
				height: (self._label.render())[1]
				theme_text_color:'Custom'
				text_color:[0,0,0,.75]
				halign:'center'
				valign: 'middle'
		BoxLayout:
			size_hint:1,None
			height:dp(20)
			spacing: dp(10)
			padding:dp(10)
			MDTextButton:
				text:'Cancel'
				font_size:dp(18)
				halign:'left'
				pos_hint:{'center_y':.5}
				custom_color:[0,0,0,.5]
				on_release: 
					root.callback(self.text,root.parameters,root)
					root.dismiss()
			Widget:
			MDTextButton:
				text:'Confirm'
				font_size:dp(20)
				halign:'right'
				custom_color:[.1,0,.2,1]
				pos_hint:{'center_y':.5}
				on_release: 
					root.callback(self.text,root.parameters,root)
					root.dismiss()
<PostOptions>
	size_hint:.9,None
	auto_dismiss: True
	pos_hint: {'center_x':.5,'center_y':.5}
	height: lay.height
	background_color:[0,0,0,.1]
	canvas:
		Color:
			rgba: [1,1,1,1]
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius:[20]
	BoxLayout:
		id:lay
		orientation: 'vertical'
		size_hint:1,None
		height:self.minimum_height
		padding:dp(5)
		spacing:dp(5)
		ButtonBoxLayout:
			size_hint: 1,None
			height: dp(50)
			padding:dp(10)
			spacing: dp(10)
			on_release:
				app.pin_user(root.post_info[1],root.root_post)
			MDIcon:
				id: pin_icon
				size_hint: None,None
				size: dp(30),dp(30)
				icon: 'pin' if root.root_post.pinned else ('pin' if root.post_info[1] in app.live_pinned_users else ('pin-off' if root.post_info[1] in app.live_unpinned_users else 'pin-off'))
				theme_text_color:'Custom'
				text_color:[.5,0,1,1] if self.icon == 'pin' else [0,0,0,1]
				pos_hint: {'center_y':.5} 
			MDLabel:
				text: 'Unpin' if pin_icon.icon == 'pin' else 'Pin'
				theme_text_color:'Custom'
				text_color:[.5,0,1,1] if pin_icon.icon == 'pin' else [0,0,0,1]
				shorten: True
		    	shorten_from: 'right'
		ButtonBoxLayout:
			size_hint: 1,None
			height: dp(50)
			padding:dp(10)
			spacing: dp(10)
			on_release:
				root.dismiss()
			MDIcon: 
				size_hint: None,None
				size: dp(30),dp(30)
				icon: 'alert-circle'
				theme_text_color:'Custom'
				text_color:[1,0,0,1]
				pos_hint: {'center_y':.5} 
			MDLabel:
				text: 'Report'
				theme_text_color:'Custom'
				text_color:[1,0,0,1]
				shorten: True
		    	shorten_from: 'right'
		ButtonBoxLayout:
			size_hint: 1,None
			height: dp(50)
			padding:dp(10)
			spacing: dp(10)
			on_release:
				app.block_user(root.post_info[1],root.root_post)
			MDIcon: 
				id:block_icon
				size_hint: None,None
				size: dp(30),dp(30)
				theme_text_color:'Custom'
				text_color:[1,0,0,1] if self.icon == 'cancel' else [0,1,0,1]
				icon: 'check-circle' if root.root_post.blocked else ('check-circle' if root.post_info[1] in app.live_blocked_users else ('cancel' if root.post_info[1] in app.live_unblocked_users else 'cancel'))
				pos_hint: {'center_y':.5} 
			MDLabel:
				text: 'Block User' if block_icon.icon == 'cancel' else 'Unblock User'
				shorten: True
				theme_text_color:'Custom'
				text_color:[1,0,0,1]if block_icon.icon == 'cancel' else [0,1,0,1]
		    	shorten_from: 'right'
<SelfPostOptions>
	size_hint:.9,None
	auto_dismiss: True
	pos_hint: {'center_x':.5,'center_y':.5}
	height: lay.height
	background_color:[0,0,0,.1]
	canvas:
		Color:
			rgba: [1,1,1,1]
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius:[20]
	BoxLayout:
		id:lay
		orientation: 'vertical'
		size_hint:1,None
		height:self.minimum_height
		padding:dp(5)
		spacing:dp(5)
		ButtonBoxLayout:
			size_hint: 1,None
			height: dp(50)
			padding:dp(10)
			spacing: dp(10)
			on_press: app.delete_post_prompt(root.post_info,root.root_post)
			on_release:
				root.dismiss()
			MDIcon: 
				size_hint: None,None
				size: dp(30),dp(30)
				icon: 'delete-forever'
				pos_hint: {'center_y':.5} 
			MDLabel:
				text: 'Delete'
				shorten: True
		    	shorten_from: 'right'
		ButtonBoxLayout:
			size_hint: 1,None
			height: dp(50)
			padding:dp(10)
			spacing: dp(10)
			on_release:
				root.dismiss()
			MDIcon: 
				size_hint: None,None
				size: dp(30),dp(30)
				icon: 'circle-edit-outline'
				pos_hint: {'center_y':.5} 
			MDLabel:
				text: 'Edit'
				shorten: True
		    	shorten_from: 'right'

<MyStackLayout>
	size_hint:None,None
	width:app.window.width-dp(50)
	height: self.minimum_height
	pos_hint:{'left':1}
	spacing:dp(5)
	
<PostTagsLayout>
	size_hint_y:None
	BoxLayout:
		id:tags_lay
		size_hint:1,1
	IconButton:
		id: more_icon
		icon: 'unfold-more-horizontal'
		size_hint:None,None
		size:dp(20),dp(20)
		font_size:dp(20)
		pos_hint:{'bottom':1}
		on_press:
			root.height = root.height+(root.real_height-root.short_height) if root.label.shorten == True else root.height-(root.real_height-root.short_height)
			root.root_layout.height = root.root_layout.height+(root.real_height-root.short_height) if root.label.shorten == True else root.root_layout.height-(root.real_height-root.short_height)
			app.adjust_scroll([root.scroll_layout,(root.real_height-root.short_height)]) if root.label.shorten == True else app.adjust_scroll([root.scroll_layout,(root.short_height-root.real_height)])
			root.parent_layout.height = root.parent_layout.height+(root.real_height-root.short_height) if root.label.shorten == True else root.parent_layout.height-(root.real_height-root.short_height)
	    	root.label.height = root.label.height+(root.real_height-root.short_height) if root.label.shorten == True else root.label.height-(root.real_height-root.short_height)
	    	root.label.shorten = False if root.label.shorten == True else True
	    	more_icon.icon = 'unfold-more-horizontal' if root.label.shorten == True else 'unfold-less-horizontal'

	Widget:
		size_hint_x:None
		width:dp(15)
<ProfileLoadingLayout>
	orientation: 'vertical'
	size_hint: 1, None
	height: (app.window.height*0.9)-dp(50)
	Widget:
		size_hint_y:None
		height:app.window.height/20
	ProgressSpinner:
		color: [0,0,1,1]
		size_hint:None,None
		size: app.window.width/6,app.window.width/6
		pos_hint:{'center_x':.5}
	Widget:
		size_hint_y:1
<MultipleImageIndex>:
	size_hint:None,None
	pos_hint:{'center_y':.5}
	size:dp(10),dp(10)
	font_size:dp(10)
	MDIcon:
		icon:'circle'
		size_hint:None,None
		size: dp(10),dp(10)
		font_size:dp(10) if root.carousel.index == root.num else dp(8)
		theme_text_color:'Custom'
		text_color:[.75,0,1,1] if root.carousel.index == root.num else [0,0,0,.5]
	"""
	)

class Pulsar(MDApp):
	window = Window
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.radii = [0]
		self.log = True
		self.user = 94
		self.user_info = []
		self.backup_user_info = [87, 'KibRafael', '_.kibzlite._', 'rapho2003', 'kibraphael7@gmail.com', '+254723983386', datetime.date(2003, 9, 7), datetime.date(2020, 4, 26), 'assets/my_pic.jpg', 'XO till we overdose\n\t\tmybad\n\t#AfterHours', 'https://www.soundcloud.com/_.kibzlite._', 28]
		self.profile_pic = ''
		self.avatar = 'assets/challenges.jpg'
		self.window.size = 360,600 #320,480   400,800    240,320
		self.window.clearcolor = [1,1,1,1]
		#self.window.fullscreen='auto'
		self.window_ratio = self.window.width/self.window.height
		self.window.softinput_mode = 'below_target'
		print(self.window.size)
		print(self.window_ratio)
		self.interests = []
		self.home_index = 0
		self.home_buffer = False
		self.post_thread_list = []
		self.displaying_posts_list = []
		self.scroll_pos_y = 0
		self.refreshed = False
		self.comments_screen = None
		self.home_screenimg = []
		self.challenge_screenimg = []
		self.my_galaxyimg = []
		self.notifications_screenimg = []
		self.gallery_images = None
		self.gallery_audio = None
		self.gallery_video = None
		self.playing_sound = None
		self.playing_sound_source = None
		self.played_sounds = []
		self.played_preview_audio = []
		self.stopped_playing_sound = None
		self.preview_audio = None
		self.preview_audio_source = None
		self.playing_video = None
		self.posting_register = []
		self.posting_tags = []
		self.live_pinned_users = []
		self.live_unpinned_users = []
		self.live_blocked_users = []
		self.live_unblocked_users = []
		self.posting_audio_lay = None
		self.posting_video_lay = None
		self.search_pics()
		self.logo = Image(source = "assets/shrine-dark.png")
		self.root = FullScreen(orientation = 'vertical',
			pos_hint={"center_y": 0.5, "center_x": 0.5}, size_hint = (1,1))
		
	def build(self):
		global logo_layout
		logo_layout = BoxLayout(orientation = "vertical", size_hint=(0.3,0.3),
		 pos_hint={"center_y": 0.5, "center_x": 0.5})
		logo_layout.add_widget(self.logo)
		self.root.add_widget(logo_layout)
		Clock.schedule_once(self.build_login, 1)
		self.dbconnection()
		return self.root
	def on_pause(self):
		print('Paused by OS')
		self.video_cache()
		if self.preview_audio:
			self.preview_audio.stop()

		return True
	def dbconnection(self):
		try:
			self.mydb = mysql.connector.connect(
			    host="localhost",
			    user="root",
			    passwd="njihia",
			    database="Pulsar"
			)
		except Exception as e:
			print("Check Your Internet Connection")
		else:
			self.mycursor = self.mydb.cursor()
		finally:
			pass
		
	def build_login(self, interval):
		self.login_screen = LoginScreen()
		if self.log == True:
			self.root.clear_widgets()
			self.build_homepage()
		else:
			self.root.add_widget(self.login_screen)

	def login(self,user,password,layout,button):
		spinner = ProgressSpinner(size_hint = (None,None),height = button.parent.height,width = button.parent.height,color = [.75,0,1,1],pos_hint={'center_x':.5})
		confirmation = MDIcon(size_hint = (None,None),height = button.parent.height,width = button.parent.height,theme_text_color = 'Custom',text_color = [0,1,0,1], icon = 'check-circle',font_size = button.parent.height,pos_hint={'center_x':.5})
		button.disabled = True
		button.parent.add_widget(spinner)
		if user == "" :
			log_popup = LoginProcessNotification()
			log_popup.ids.log_message.text = "Your Username is required"
			log_popup.ids.log_message.text_color = [1,0,0,1]
			layout.clear_widgets()
			layout.add_widget(log_popup)
			button.disabled = False
			button.parent.remove_widget(spinner)
		elif password == "":
			log_popup = LoginProcessNotification()
			log_popup.ids.log_message.text = "Your Password is required"
			log_popup.ids.log_message.text_color = [1,0,0,1]
			layout.clear_widgets()
			layout.add_widget(log_popup)
			button.disabled = False
			button.parent.remove_widget(spinner)
		else:
			log_popup = LoginProcessNotification()
			log_popup.ids.log_message.text = "Authenticating..."
			log_popup.ids.log_message.text_color = [.5,0,1,1]
			layout.clear_widgets()
			layout.add_widget(log_popup)
			login_sql = "SELECT `Userid`, `Username`, `Password` FROM `users` WHERE Username = %s AND Password = %s"
			values = (user,password)
			try:
				self.dbconnection()
				self.mycursor.execute(login_sql, values)
				myresult = self.mycursor.fetchone()
			except Exception as e:
				log_popup.ids.log_message.text = "Check your Internet Connection"
				log_popup.ids.log_message.text_color = [1,0,0,1]
				button.disabled = False
				button.parent.remove_widget(spinner)
			else:
				if myresult == None:
					log_popup.ids.log_message.text = "Invalid Username or Password"
					log_popup.ids.log_message.text_color = [1,0,0,1]
					button.disabled = False
					button.parent.remove_widget(spinner)
				else:
					button.parent.remove_widget(spinner)
					button.parent.add_widget(confirmation)
					log_popup.ids.log_message.text = "Login is Successful"
					log_popup.ids.log_message.text_color = [0,1,0,1]
					self.user = myresult[0]
					Clock.schedule_once(partial(self.welcome,'login'), 2)
					

	def signup(self, user, email, phone, password,layout,button):
		spinner = ProgressSpinner(size_hint = (None,None),height = button.parent.height,width = button.parent.height,color = [.75,0,1,1],pos_hint={'center_x':.5})
		confirmation = MDIcon(size_hint = (None,None),height = button.parent.height,width = button.parent.height,theme_text_color = 'Custom',text_color = [0,1,0,1], icon = 'check-circle',font_size = button.parent.height,pos_hint={'center_x':.5})
		button.disabled = True
		button.parent.add_widget(spinner)
		if user == "" or password == "":
			log_popup = LoginProcessNotification()
			log_popup.ids.log_message.text = "Your name and Password are required"
			log_popup.ids.log_message.text_color = [1,0,0,1]
			layout.clear_widgets()
			layout.add_widget(log_popup)
			button.disabled = False
			button.parent.remove_widget(spinner)
		else:
			log_popup = LoginProcessNotification()
			log_popup.ids.log_message.text = "Submitting..."
			log_popup.ids.log_message.text_color = [.5,0,1,1]
			layout.clear_widgets()
			layout.add_widget(log_popup)
			login_sql = "SELECT `Userid`, `Username`, `Password` FROM `users` WHERE Username = %s OR Userid = %s"
			values = [user,user]
			try:
				self.dbconnection()
				self.mycursor.execute(login_sql,values)
				myresult = self.mycursor.fetchall()
			except Exception as e:
				log_popup.ids.log_message.text = "Check your Internet Connection"
				log_popup.ids.log_message.text_color = [1,0,0,1]
				layout.clear_widgets()
				layout.add_widget(log_popup)
				button.disabled = False
				button.parent.remove_widget(spinner)
			else:
				if myresult == []:
					today = datetime.date.today()
					signup_sql = "INSERT INTO `users`(`FullName`, `Username`, `Password`, `Email`, `Phone`, `DOR`) VALUES (%s,%s,%s,%s,%s,%s)"
					values =(user,user,password,email,phone, today)
					try:
						self.dbconnection()
						self.mycursor.execute(signup_sql, values)
						self.mydb.commit()
						login_sql = "SELECT `Userid`, `Username`, `Password` FROM `users` WHERE Username = %s AND Password = %s"
						values = (user,password)
						self.mycursor.execute(login_sql, values)
						my_result = self.mycursor.fetchone()
						self.user_info = my_result
						'''
						user = auth.create_user(
							uid = str(my_result[0]),email = email,email_verified = False,display_name = user,password = password
							) 
						custom_token = auth.create_custom_token(user.uid)
						print(custom_token)
						'''
					except Exception as e:
						print(type(e))
						log_popup.ids.log_message.text = "Check your Internet Connection"
						log_popup.ids.log_message.text_color = [1,0,0,1]
						layout.clear_widgets()
						layout.add_widget(log_popup)
						button.disabled = False
						button.parent.remove_widget(spinner)
					else:
						button.parent.remove_widget(spinner)
						button.parent.add_widget(confirmation)
						log_popup.ids.log_message.text = "Account Created Successfully"
						log_popup.ids.log_message.text_color = [0,1,0,1]
						self.user=my_result[0]
						Clock.schedule_once(partial(self.welcome,'signup'), 2)
				else:
					log_popup.ids.log_message.text = "Sorry, your Username has already been given out"
					log_popup.ids.log_message.text_color = [1,0,1,1]
					button.parent.remove_widget(spinner)
					button.disabled = button.disabled
					layout.clear_widgets()
					layout.add_widget(log_popup)
	def welcome(self,mode,instance):
		global logo_layout
		self.log = True
		self.root.clear_widgets()
		logo_layout.clear_widgets()
		if mode == 'login':
			self.build()
		else:
			self.Interests()
	def Interests (self):
		self.interests_screen = InterestScreen()
		interests = self.interests_db_search()
		for i in interests:
			d= i[2]
			sub_interest_sql = "SELECT sub_interest_name, id, sub_interest_id, icon FROM sub_interests WHERE interest_id = %d"%d
			self.mycursor.execute(sub_interest_sql)
			sub_interests = self.mycursor.fetchall()
			interest = InterestCard(source = str(i[3]), pres = 'sub_interests',sub = sub_interests,idd = str(i[2]))
			interest.ids.interest_category.text = str(i[1])
			self.interests_screen.ids.interests_scroll.add_widget(interest)
		self.root.add_widget(self.interests_screen)
	def interests_db_search(self):
		interest_sql = "SELECT * FROM interests"
		self.mycursor.execute(interest_sql)
		interests = self.mycursor.fetchall()
		return interests

	def interest_subcategory(self, check, idd, state,layout,sub):
		if check.icon == 'checkbox-blank-circle-outline' or (state== 'pic' and check.icon == 'checkbox-marked-circle-outline'):
			if state == 'pic':
				if layout.occupied == 'No':
					for i in sub:
						interest_subcategory = InterestSubcategory(source = str(i[3]), pres = 'select_interest', idd = str(i[2]))
						if str(i[2]) in self.interests:
							interest_subcategory.ids.interest_check.icon = 'checkbox-marked-circle-outline'
						else:
							pass
						interest_subcategory.ids.subinterests_title.text = str(i[0])
						layout.height+=(interest_subcategory.height+dp(1))
						layout.add_widget(interest_subcategory)
						layout.occupied = 'Yes'
				
				else:
					if state == 'pic' and layout.occupied == 'Yes' and check.icon == 'checkbox-blank-circle-outline':
						self.select_interest(check,idd)
					else:
						print(state+check.icon)
						layout.clear_widgets()
						layout.occupied = 'No'
						layout.height = dp(0)
				if check.icon == 'checkbox-blank-circle-outline':
					self.select_interest(check,idd)
			else:
				self.select_interest(check, idd)
			
		else:
			self.select_interest(check, idd)
			
	def select_interest(self,check, idd):
		print(idd)
		# maintain state even after dismiss modalview
		count = int(self.interests_screen.ids.interest_count.text)
		if check.icon=='checkbox-blank-circle-outline':
			self.interests.append(idd)
			count+=1
			self.interests_screen.ids.interest_count.text = str(count)
			check.icon ='checkbox-marked-circle-outline'
		else:
			print(self.interests)
			print(idd)
			self.interests.remove(idd)
			count-=1
			self.interests_screen.ids.interest_count.text = str(count)
			check.icon ='checkbox-blank-circle-outline'
	def save_interests(self):
		#research on how to check for repetition in a list
		#and remove repetition while requesting for interests
		log_popup = LoginProcess()
		log_popup.ids.log_message.text = "Submitting...."
		log_popup.open()
		print(self.interests)
		print(self.user)
		insert_interest_sql = "INSERT INTO `user_interests`(`interest_id`, `user_id`) VALUES (%s,%s)"
		try:
			self.dbconnection()
			for i in self.interests:
				values =(i,self.user)
				self.mycursor.execute(insert_interest_sql, values)
			self.mydb.commit()
		except:
			log_popup.ids.log_message.text = "Check your Internet Connection"
			log_popup.ids.log_process_layout.remove_widget(log_popup.ids.log_spinner)
			log_popup.auto_dismiss = True
		else:
			log_popup.dismiss()
			self.root.clear_widgets()
			self.build()

	def build_homepage(self):
		interests_sql = "SELECT `interest_id` FROM `user_interests` WHERE user_id = %s"%self.user
		user_sql = "SELECT * FROM `users` WHERE UserId = %s OR DOR = %s"
		try:
			self.dbconnection()
			if self.interests == []:
				self.mycursor.execute(interests_sql)
				myresult = self.mycursor.fetchall()
				self.interests = myresult
			self.mycursor.execute(user_sql,[self.user,self.user])
			result = self.mycursor.fetchone()
			self.user_info = result
			if self.user_info[8] == '':
				self.profile_pic = self.avatar
			else:
				self.profile_pic = self.user_info[8]
			print(self.user_info)
			self.user_post_count = result[11]
		except Exception as e:
			print(e)
			self.profile_pic = self.avatar
			print('Check your Internet Connection')
		self.root_manager = RootManager()
		self.root_screen = self.root_manager.ids.rootscreen
		self.root_manager.ids.myprofile.source = self.profile_pic
		self.home_page = HomePage()
		self.root_screen.add_widget(self.home_page)
		self.my_galaxy = MyGalaxy()
		self.root_screen.add_widget(self.my_galaxy)
		self.challenge_screen = ChallengeScreen()
		self.root_screen.add_widget(self.challenge_screen)
		#self.notification_screen = NotificationScreen()
		#self.root_screen.add_widget(self.notification_screen)
		self.my_profile = MyProfileScreen()
		self.root_screen.add_widget(self.my_profile)
		self.post_screen = PostScreen()
		self.post_screen.ids.profile_pic.source = self.profile_pic
		self.root_manager.add_widget(self.post_screen)
		self.camera_screen = CameraScreen()
		self.root_manager.add_widget(self.camera_screen)
		self.menu_screen = MenuScreen()
		self.root_manager.add_widget(self.menu_screen)
		#self.messages_screen = MessageScreen()
		#self.root_manager.add_widget(self.messages_screen)
		self.root.add_widget(self.root_manager)

	def display_posts(self, instance):
		posts_sql = "SELECT x.* FROM (SELECT posts.id,posts.UserId,posts.post_id,posts.caption,posts.type,posts.image_ratio,users.Username,users.ProfilePicture,posts.emotion,posts.time FROM `posts` INNER JOIN `users` ON posts.Userid = users.Userid WHERE EXISTS (SELECT 1 from pins WHERE pins.pinned_id = users.Userid AND pins.Userid = %s) AND NOT EXISTS (SELECT 1 from blocked_users WHERE blocked_users.blocked_user = users.Userid AND blocked_users.Userid = %s) UNION SELECT posts.id,users.UserId,posts.post_id,posts.caption,posts.type,posts.image_ratio,users.Username,users.ProfilePicture,CONCAT('@',poster.Username),posts.time FROM `reposts` INNER JOIN `posts` INNER JOIN `users` ON posts.post_id = reposts.post_id AND reposts.Userid = users.Userid INNER JOIN `users` AS poster ON posts.Userid = poster.Userid WHERE EXISTS (SELECT 1 from pins WHERE pins.pinned_id = users.Userid AND pins.Userid = %s) AND NOT EXISTS (SELECT 1 from blocked_users WHERE blocked_users.blocked_user = users.Userid AND blocked_users.Userid = %s))x ORDER BY x.time DESC, x.id DESC LIMIT %s OFFSET %s" #LIMIT 10 OFFSET 0
		try:
			self.dbconnection()
			self.mycursor.execute(posts_sql,[self.user,self.user,self.user,self.user,10,self.home_index*10])
			myresult = self.mycursor.fetchall()
			if self.home_buffer==False:
				self.home_page.ids.recycle_layout.clear_widgets()
			self.displaying_posts_list = [self.home_page.ids.recycle_layout,0]
			for i in myresult:
				sub_info = self.check_sub_info(i)
				if i[4] == 'Image':
					post_images_sql = "SELECT * FROM `post_images` WHERE `post_id` = %s OR `id`= %s"
					post_images_values = [i[2],i[2]]
					self.dbconnection()
					self.mycursor.execute(post_images_sql,post_images_values)
					result = self.mycursor.fetchall()
				elif i[4] == 'Audio':
					post_audio_sql = "SELECT * FROM `post_audio` WHERE `post_id` = %s OR `id`= %s"
					post_audio_values = [i[2],i[2]]
					self.dbconnection()
					self.mycursor.execute(post_audio_sql,post_audio_values)
					result = self.mycursor.fetchone()
					
				elif i[4] == 'Video':
					post_video_sql = "SELECT * FROM `post_video` WHERE `post_id` = %s OR `id`= %s"
					post_video_values = [i[2],i[2]]
					self.dbconnection()
					self.mycursor.execute(post_video_sql,post_video_values)
					result = self.mycursor.fetchone()
				self.post_thread_list.clear()
				self.display_a_post(i,result,self.home_page.ids.recycle_layout,sub_info,self.home_page.ids.recycle_layout)
		
		except Exception as e:
			raise e
			toast('Check Your Internet Connection')
			'''
		try:
			if myresult != []:
				interval_object = PeopleLayout(title = 'Discover People')
				interval_layout = BoxLayout(orientation = 'vertical',size_hint = (None,None),size = (self.window.width,interval_object.height))
				interval_layout.add_widget(FullSeparator(pos_hint = {'top':1}))
				interval_layout.add_widget(interval_object)
				interval_layout.add_widget(FullSeparator(pos_hint = {'bottom':1}))
				print(interval_layout.height)
				print(interval_object.height)
				self.home_page.ids.recycle_layout.add_widget(interval_layout)
				self.displaying_posts_list[1]+=(interval_object.height+dp(18))
			else:
				print(myresult)
		except:
			pass
			'''
		print(str('This works outside IDLE! \U0001F44D'))
		self.adjust_scroll(self.displaying_posts_list)
		print('done')
		if self.refreshed == True:
			self.refresh_done()
		if self.home_buffer == True:
			self.buffer_done()
	def check_sub_info(self,i):
		sub_info = []
		check_like_sql = "SELECT * FROM `likes` WHERE `post_id` = %s AND `Userid`= %s"
		check_repost_sql = "SELECT * FROM `reposts` WHERE `post_id` = %s AND `Userid`= %s"
		check_save_sql = "SELECT * FROM `post_saves` WHERE `post_id` = %s AND `Userid`= %s"
		check_pin_sql = "SELECT * FROM `pins` WHERE Userid = %s AND pinned_id = %s"
		count_likes_sql = "SELECT COUNT(*) FROM `likes` WHERE `post_id` = %s OR `Userid`= %s"
		count_comments_sql = "SELECT COUNT(*) FROM `comments` WHERE `post_id` = %s OR `Userid`= %s"
		get_tags_sql = "SELECT * FROM `tags` WHERE `post_id` = %s OR `post_id`= %s"
		check_block_sql = "SELECT * FROM `blocked_users` WHERE Userid = %s AND blocked_user = %s"
		like_values = (i[2],self.user)
		self.mycursor.execute(check_like_sql, like_values)
		like_result = self.mycursor.fetchone()
		if like_result == None:
			sub_info.append('heart-outline')
		else:
			sub_info.append('heart')
		self.mycursor.execute(count_likes_sql,[i[2],i[2]])
		likes_result = self.mycursor.fetchone()
		like_count= ''.join(map(str, likes_result))
		sub_info.append(int(like_count))
		self.mycursor.execute(count_comments_sql,[i[2],i[2]])
		comments_result = self.mycursor.fetchone()
		comment_count= ''.join(map(str, comments_result))
		sub_info.append(int(comment_count))
		self.mycursor.execute(check_repost_sql, like_values)
		repost_result = self.mycursor.fetchone()
		if repost_result == None:
			sub_info.append('repeat')
		else:
			sub_info.append('repeat-once')
		self.mycursor.execute(check_save_sql, like_values)
		save_result = self.mycursor.fetchone()
		if save_result == None:
			sub_info.append('bookmark-outline')
		else:
			sub_info.append('bookmark')
		self.mycursor.execute(check_pin_sql, [self.user,i[1]])
		pin_result = self.mycursor.fetchone()
		if pin_result == None:
			sub_info.append(False)
		else:
			sub_info.append(True)
		self.mycursor.execute(get_tags_sql, [i[2],i[2]])
		tags_result = self.mycursor.fetchall()
		sub_info.append(tags_result)
		self.mycursor.execute(check_block_sql, [self.user,i[1]])
		block_result = self.mycursor.fetchone()
		if block_result == None:
			sub_info.append(False)
		else:
			sub_info.append(True)
		return sub_info
	def display_a_post(self,info,media,layout,sub_info,outer_layout):
		if info[4] == 'Image':
			i_r = info[5]
			h = (self.window.width)/i_r
			a_g = h
			if info[7] == '':
				profile_pic = self.avatar
			else:
				profile_pic = info[7]
			if h > ((self.window.height)-dp(60)):
				n_hg = ((self.window.height)-dp(60))
				a_g = n_hg
				if len(media) == 1:
					post = ImageLayout(virtual_height = n_hg+dp(61),source = media[0][2], post_height = n_hg,username = info[6], profilepic = profile_pic,post_info = info)
				else:
					post = ImageLayoutMultiple(virtual_height = n_hg+dp(61),source = media[0][2], post_height = n_hg,username = info[6], profilepic = profile_pic,post_info = info)
				post.ids.blur.ratio = 1/info[5]
				post.ids.image_blur.effects = [PixelateEffect(pixel_size = 1.5),HorizontalBlurEffect(size = 15)]
				post.ids.image.size_hint = (None,1)
				post.ids.image.size = (n_hg*info[5],n_hg)
			else:
				if len(media) == 1:
					pass
					post = ImageLayout(virtual_height = h+dp(61), source = media[0][2], post_height = h,username = info[6], profilepic = profile_pic,post_info = info)
					#post = DebugImageLayout(source = media[0][2], post_height = h,username = info[6], profilepic = info[7],post_info = info)
				else:
					post = ImageLayoutMultiple(virtual_height = h+dp(61), source = media[0][2], post_height = h,username = info[6], profilepic = profile_pic,post_info = info)
			post.ids.like_icon.icon = sub_info[0]
			post.ids.caption.text = info[3]
			post.emotion = info[8]
			if info[8] == '':
				post.ids.emotion.parent.remove_widget(post.ids.emotion)
			before = post.ids.caption._label.render()
			post.ids.caption.text_size=((self.window.width - dp(50)), None)
			after = post.ids.caption._label.render()
			if post.ids.caption.text == '':
				post.ids.caption.height = 0
				post.ids.caption_lay.parent.remove_widget(post.ids.caption_lay)
			else:
				post.ids.caption.virtual_height = (after[1]/before[1])*before[1]
				post.ids.caption.shorten = True
				_before = post.ids.caption._label.render()
				post.ids.caption.text_size=((self.window.width - dp(50)), None)
				_after = post.ids.caption._label.render()
				post.ids.caption.height = (_after[1]/_before[1])*_before[1]
				post.ids.caption.short_height = (_after[1]/_before[1])*_before[1]
				if post.ids.caption.short_height == post.ids.caption.virtual_height:
					post.ids.caption_lay.remove_widget(post.ids.caption_button)
			post.scroll_layout = outer_layout
			info_height = post.ids.caption.height
			like = LikeComment()
			like.ids.comment_lay.ids.profile_pic.source = self.profile_pic
			post.likecomment = like
			like.likes = sub_info[1]
			like.comments =  sub_info[2]
			like.post_info = info
			rate = Rate()
			rate.post_info = info
			rate.ids.repost_icon.icon = sub_info[3]
			rate.ids.save_icon.icon = sub_info[4]
			post.pinned = sub_info[5]
			post.blocked = sub_info[7]
			posted_time = info[9]
			diff = post_timestamp(posted_time)
			time = Time(time = str(diff))
			tags_layout = PostTagsLayout(orientation ='horizontal', size_hint_y = None)
			tags = MyStackLayout()
			taglabel = TagCard(text_size=(None, None),font_size = dp(15), size_hint_y=None,text = '',tag_info = 'tags',pos_hint={'center_y':.5})
			tags_list = sub_info[6]
			for i in tags_list:
				txt = " [ref=%s][color=301099]%s[/color][/ref] "%(str(i[1]),str(i[1]))
				taglabel.text = taglabel.text+txt
			before = taglabel._label.render()
			taglabel.text_size=(self.window.width-dp(50), None)
			after = taglabel._label.render()
			if (after[1]/before[1])>2:
				real_height = (after[1]/before[1])*before[1]
				taglabel.shorten = True
				taglabel.shorten_from = 'right'
				taglabel.text_size=(None, None)
				before = taglabel._label.render()
				taglabel.text_size=(self.window.width-dp(50), None)
				after = taglabel._label.render()
				taglabel.height = (after[1]/before[1])*before[1]
				tags_layout.real_height = real_height
				tags_layout.short_height = (after[1]/before[1])*before[1]
				tags_layout.parent_layout = post.ids.post_info
				tags_layout.root_layout = post
				tags_layout.scroll_layout = outer_layout
				tags_layout.label = taglabel
			else:
				taglabel.height = (after[1]/before[1])*before[1]
				tags_layout.remove_widget(tags_layout.ids.more_icon)
			if taglabel.text!=0:
				tags.add_widget(taglabel)
				tags.height = taglabel.height
				tags_layout.height = tags.height
				tags_layout.ids.tags_lay.add_widget(tags)
				post.ids.post_info.add_widget(tags_layout)
			if sub_info[1] == 0 and sub_info[2] == 0:
				comment = CommentLay()
				comment.post_info = info
				comment.ids.profile_pic.source = self.profile_pic
				like_height = comment.height
				post.ids.post_info.add_widget(comment)
			else:
				post.ids.post_info.add_widget(like)
				like_height = like.height
				if sub_info[1] == 0:
					like.ids.likes_button.parent.remove_widget(like.ids.likes_button)
				if sub_info[2] == 0:
					like.ids.comments_button.parent.remove_widget(like.ids.comments_button)
			if info[1]!= self.user:
				post.ids.post_info.add_widget(rate)
				rate_height = rate.height
			else:
				rate_height = 0
			post_info_height = info_height+tags.height+rate_height+like_height+dp(20)
			post.info = post_info_height
			post.ids.post_info.add_widget(time)
			additional_pics = []
			additional_pics.clear()
			if len(media)>1:
				for i in range(len(media)):
					multiple_index = MultipleImageIndex(num = i,carousel = post.ids.carousel)
					post.ids.multiple_index.add_widget(multiple_index)
				for i in range(1,(len(media))):
					additional_pics.append(media[i])
				for i in additional_pics:
					img_trial = Image(source = i[2],keep_ratio = True,allow_stretch = True,size_hint =(None,None))
					w = self.window.width
					h = a_g
					i_r = w/h
					ir = img_trial.image_ratio
					#if i[2].endswith(".png"):
					#	box = RelativeLayout(size_hint= (1, 1),pos_hint = {'center_y': .5})
					#else:
					box = RelativeLayout(size_hint= (1, 1),pos_hint = {'center_y': .5})
					bg = ImageBGEXT(source = i[2], size_hint= (1, 1),pos_hint = {'center_y': .5})
					bge = EffectWidget(effects = [PixelateEffect(pixel_size = 1.5),HorizontalBlurEffect(size = 25)],size_hint= (1, 1),pos_hint = {'center_y': .5})
					bge.add_widget(bg)
					box.add_widget(bge)
					#Add a condition not to add the bg if it is .png
					if ir>i_r:
						img = ImageTouch(source= i[2],allow_stretch=True, size_hint= (None, None),pos_hint = {'center_y': .5,'center_x': .5})
						img.width = w
						img.height = img.width/img.image_ratio
						box.add_widget(img)
					else:
						img = ImageTouch(source= i[2],allow_stretch=True, size_hint= (None, None),pos_hint = {'center_y': .5,'center_x': .5})
						img.height = h
						img.width = img.height*img.image_ratio
						#bg.add_widget(Widget())
						box.add_widget(img)
						#bg.add_widget(Widget())
					post.ids.carousel.add_widget(box)
			layout.add_widget(post)
			post_estimate_height = h+dp(61)+post_info_height
			self.displaying_posts_list[1]+=(post.height+dp(18))
			print('image'+str(post.height))

		elif info[4] == 'Audio':
			if info[7] == '':
				profile_pic = self.avatar
			else:
				profile_pic = info[7]
			post = AudioLayout(source = media[2],cover = media[6],username = info[6], profilepic = profile_pic,title = media[4],post_info = info)
			post.ids.like_icon.icon = sub_info[0]
			post.ids.caption.text = info[3]
			post.emotion = info[8]
			before = post.ids.caption._label.render()
			post.ids.caption.text_size=((self.window.width - dp(50)), None)
			after = post.ids.caption._label.render()
			if post.ids.caption.text == '':
				post.ids.caption.height = 0
				post.ids.caption_lay.parent.remove_widget(post.ids.caption_lay)
			else:
				post.ids.caption.virtual_height = (after[1]/before[1])*before[1]
				post.ids.caption.shorten = True
				_before = post.ids.caption._label.render()
				post.ids.caption.text_size=((self.window.width - dp(50)), None)
				_after = post.ids.caption._label.render()
				post.ids.caption.height = (_after[1]/_before[1])*_before[1]
				post.ids.caption.short_height = (_after[1]/_before[1])*_before[1]
				if post.ids.caption.short_height == post.ids.caption.virtual_height:
					post.ids.caption_lay.remove_widget(post.ids.caption_button)
			post.scroll_layout = outer_layout
			info_height = post.ids.caption.height
			post.likes = sub_info[1]
			post.comments =  sub_info[2]
			post.like_comment_info = info
			rate = Rate()
			rate.post_info = info
			rate.ids.repost_icon.icon = sub_info[3]
			rate.ids.save_icon.icon = sub_info[4]
			post.pinned = sub_info[5]
			post.blocked = sub_info[7]
			posted_time = info[9]
			diff = post_timestamp(posted_time)
			time = Time(time = str(diff))
			tags_layout = PostTagsLayout(orientation ='horizontal', size_hint_y = None)
			tags = MyStackLayout()
			taglabel = TagCard(text_size=(None, None),font_size = dp(15), size_hint_y=None,text = '',tag_info = 'tags',pos_hint={'center_y':.5})
			tags_list = sub_info[6]
			for i in tags_list:
				txt = " [ref=%s][color=301099]%s[/color][/ref] "%(str(i[1]),str(i[1]))
				taglabel.text = taglabel.text+txt
			before = taglabel._label.render()
			taglabel.text_size=(self.window.width-dp(50), None)
			after = taglabel._label.render()
			if (after[1]/before[1])>2:
				real_height = (after[1]/before[1])*before[1]
				taglabel.shorten = True
				taglabel.shorten_from = 'right'
				taglabel.text_size=(None, None)
				before = taglabel._label.render()
				taglabel.text_size=(self.window.width-dp(50), None)
				after = taglabel._label.render()
				taglabel.height = (after[1]/before[1])*before[1]
				tags_layout.real_height = real_height
				tags_layout.short_height = (after[1]/before[1])*before[1]
				tags_layout.parent_layout = post.ids.post_info
				tags_layout.root_layout = post
				tags_layout.scroll_layout = outer_layout
				tags_layout.label = taglabel
			else:
				taglabel.height = (after[1]/before[1])*before[1]
				tags_layout.remove_widget(tags_layout.ids.more_icon)
			if taglabel.text!=0:
				tags.add_widget(taglabel)
				tags.height = taglabel.height
				tags_layout.height = tags.height
				tags_layout.ids.tags_lay.add_widget(tags)
				post.ids.post_info.add_widget(tags_layout)
			if info[1]!= self.user:
				post.ids.post_info.add_widget(rate)
				rate_height = rate.height
			else:
				rate_height = 0
			post.info = info_height+tags.height+rate_height+dp(20)
			post.ids.post_info.add_widget(time)
			layout.add_widget(post)
			self.displaying_posts_list[1]+=(post.info + dp(50)+(self.window.width/5)+dp(18)    -dp(20))#remove the -dp(20)

		elif info[4] == 'Video':
			hg = (self.window.width)/(info[5])
			if info[7] == '':
				profile_pic = self.avatar
			else:
				profile_pic = info[7]
			if hg > ((self.window.height)-dp(60)):
				n_hg = ((self.window.height)-dp(60))
				v_g = n_hg
				post = VideoLayout(virtual_height = n_hg+dp(61),thumbnail = media[4],source = media[2], post_height = n_hg,username = info[6], profilepic = profile_pic,post_info = info)
				post.ids.post_video.ids.blur.ratio = 1/info[5]
				post.ids.post_video.ids.video_blur.effects = [PixelateEffect(pixel_size = 1.5),HorizontalBlurEffect(size = 15)]


			else:
				v_g = hg
				post = VideoLayout(virtual_height = hg+dp(61),thumbnail = media[4],source = media[2], post_height = hg,username = info[6], profilepic = profile_pic,post_info = info)
			post.ids.like_icon.icon = sub_info[0]
			post.ids.caption.text = info[3]
			post.emotion = info[8]
			if info[8] == '':
				post.ids.emotion.parent.remove_widget(post.ids.emotion)
			before = post.ids.caption._label.render()
			post.ids.caption.text_size=((self.window.width - dp(50)), None)
			after = post.ids.caption._label.render()
			if post.ids.caption.text == '':
				post.ids.caption.height = 0
				post.ids.caption_lay.parent.remove_widget(post.ids.caption_lay)
			else:
				post.ids.caption.virtual_height = (after[1]/before[1])*before[1]
				post.ids.caption.shorten = True
				_before = post.ids.caption._label.render()
				post.ids.caption.text_size=((self.window.width - dp(50)), None)
				_after = post.ids.caption._label.render()
				post.ids.caption.height = (_after[1]/_before[1])*_before[1]
				post.ids.caption.short_height = (_after[1]/_before[1])*_before[1]
				if post.ids.caption.short_height == post.ids.caption.virtual_height:
					post.ids.caption_lay.remove_widget(post.ids.caption_button)
			post.scroll_layout = outer_layout
			info_height = post.ids.caption.height
			like = LikeComment()
			like.ids.comment_lay.ids.profile_pic.source = self.profile_pic
			like.likes = sub_info[1]
			like.comments =  sub_info[2]
			post.likecomment = like
			like.post_info = info
			rate = Rate()
			rate.post_info = info
			rate.ids.repost_icon.icon = sub_info[3]
			rate.ids.save_icon.icon = sub_info[4]
			post.pinned = sub_info[5]
			post.blocked = sub_info[7]
			posted_time = info[9]
			diff = post_timestamp(posted_time)
			time = Time(time = str(diff))
			tags_layout = PostTagsLayout(orientation ='horizontal', size_hint_y = None)
			tags = MyStackLayout()
			taglabel = TagCard(text_size=(None, None),font_size = dp(15), size_hint_y=None,text = '',tag_info = 'tags',pos_hint={'center_y':.5})
			tags_list = sub_info[6]
			for i in tags_list:
				txt = " [ref=%s][color=301099]%s[/color][/ref] "%(str(i[1]),str(i[1]))
				print(txt)
				taglabel.text = taglabel.text+txt
			before = taglabel._label.render()
			taglabel.text_size=(self.window.width-dp(50), None)
			after = taglabel._label.render()
			if (after[1]/before[1])>2:
				real_height = (after[1]/before[1])*before[1]
				taglabel.shorten = True
				taglabel.shorten_from = 'right'
				taglabel.text_size=(None, None)
				before = taglabel._label.render()
				taglabel.text_size=(self.window.width-dp(50), None)
				after = taglabel._label.render()
				taglabel.height = (after[1]/before[1])*before[1]
				tags_layout.real_height = real_height
				tags_layout.short_height = (after[1]/before[1])*before[1]
				tags_layout.parent_layout = post.ids.post_info
				tags_layout.root_layout = post
				tags_layout.scroll_layout = outer_layout
				tags_layout.label = taglabel
			else:
				taglabel.height = (after[1]/before[1])*before[1]
				tags_layout.remove_widget(tags_layout.ids.more_icon)
			if taglabel.text!=0:
				tags.add_widget(taglabel)
				tags.height = taglabel.height
				tags_layout.height = tags.height
				tags_layout.ids.tags_lay.add_widget(tags)
				post.ids.post_info.add_widget(tags_layout)
			if sub_info[1] == 0 and sub_info[2] == 0:
				comment = CommentLay()
				comment.post_info = info
				comment.ids.profile_pic.source = self.profile_pic
				like_height = comment.height
				post.ids.post_info.add_widget(comment)
			else:
				post.ids.post_info.add_widget(like)
				like_height = like.height
				if sub_info[1] == 0:
					like.ids.likes_button.parent.remove_widget(like.ids.likes_button)
				if sub_info[2] == 0:
					like.ids.comments_button.parent.remove_widget(like.ids.comments_button)
			if info[1]!= self.user:
				post.ids.post_info.add_widget(rate)
				rate_height = rate.height
			else:
				rate_height = 0
			post.info = info_height+tags_layout.height+rate_height+like_height+dp(20)
			post.ids.post_info.add_widget(time)
			layout.add_widget(post)
			self.displaying_posts_list[1]+=(post.height)
			print('video'+str(post.height))
	def adjust_scroll(self,parameters):
		print(parameters)
		vp_height = parameters[0].parent.viewport_size[1]
		print('height'+str(vp_height))
		print('added'+str(parameters[1]))
		sv_height = parameters[0].parent.height
		print(vp_height, sv_height)
		if vp_height > sv_height:
			scroll = parameters[0].parent.scroll_y
			print(scroll)
			bottom = scroll * (vp_height - sv_height)
			print(bottom)
			Clock.schedule_once(partial(self.adjust_scroll_callback,parameters, bottom+parameters[1]), -1)
	def adjust_scroll_callback(self,parameters,bottom,dt):
		vp_height = parameters[0].parent.viewport_size[1]
		print('newheight'+str(vp_height))
		sv_height = parameters[0].parent.height
		parameters[0].parent.scroll_y = bottom / (vp_height - sv_height)
		print(vp_height,sv_height)
		print(bottom)
		print( bottom / (vp_height - sv_height))
	def adjust_scroll_special(self,parameters):
		print(parameters)
		vp_height = parameters[0].parent.viewport_size[1]
		sv_height = parameters[0].parent.height
		print(vp_height, sv_height)
		if vp_height > sv_height:
			scroll = parameters[0].parent.scroll_y
			print(scroll)
			bottom = scroll * (vp_height - sv_height)
			print(bottom)
			Clock.schedule_once(partial(self.adjust_scroll_special_callback,parameters, bottom+parameters[1]), -1)
	def adjust_scroll_special_callback(self,parameters,bottom,dt):
		vp_height = parameters[0].parent.viewport_size[1]
		sv_height = parameters[0].parent.height
		parameters[0].parent.scroll_y = bottom / (vp_height - sv_height)
		print(vp_height,sv_height)
		print(vp_height - sv_height)
		print( bottom / (vp_height - sv_height))
	def video_play(self,video,thumbnail, icon):
		if video.state == 'pause':
			anim = Animation(opacity = 0,t = 'linear')
			anim.start(icon)
		else:
			anim = Animation(opacity = 1,t = 'linear')
			anim.start(icon)
	def audio_video_pause(self):
		if self.playing_sound and self.playing_sound.state == 'play':
			self.playing_sound.stop()
			self.stopped_playing_sound = self.playing_sound
			for i in self.played_sounds:
				i[0].icon = 'play'
				print(i)
	def audio_video_play(self):
		if self.stopped_playing_sound:
			time.sleep(.2)
			self.stopped_playing_sound.play()
			self.stopped_playing_sound = None
			for i in self.played_sounds:
				if self.playing_sound_source == i[1]:
					i[0].icon = 'pause'
	def video_auto_pause(self,video,layout):
		print(video,layout)
		scroll_pos = layout.parent.parent.scroll_y
		async def some_task():
			await thread(partial(self.video_auto_pause_thread,scroll_pos,video,layout, 0))
		ak.start(some_task())
	def video_auto_pause_thread(self,scroll_pos,video,layout,instance):
		timeout = (layout.parent.parent.height/2)+(video.height/8)
		while True:
			new_scroll_pos = layout.parent.parent.scroll_y
			scroll_distance = (new_scroll_pos-scroll_pos)*layout.parent.parent.viewport_size[1]
			if scroll_distance>timeout or scroll_distance<(-1*timeout):
				video.state = 'pause'
				break
			if video.state == 'pause' or video.state == 'stop':
				break
			time.sleep(.25)
	def passs(self):
		pass

	def play_audio(self, sound):
		self.video_cache()
		if self.playing_sound and self.playing_sound_source == sound:
			self.playing_sound.play()
		else:
			if self.playing_sound:
				self.playing_sound.stop()
			self.playing_sound = SoundLoader.load(sound)
			self.playing_sound_source = sound
			self.playing_sound.play()
			for i in self.played_sounds:
				if self.playing_sound and self.playing_sound_source == i[1] and self.playing_sound.state== 'stop':
					i[0].icon = 'play'
				elif self.playing_sound and self.playing_sound_source == i[1]:
					i[0].icon = 'pause'
				else:
					i[0].icon = 'play'
			self.played_sounds.clear()

	def pause_audio(self):
		if self.playing_sound:
			self.playing_sound.stop()
		if self.stopped_playing_sound:
			self.stopped_playing_sound = None
	def preview_audio_play(self,sound):
		self.video_cache()
		if self.playing_sound and self.playing_sound.state == 'play':
			self.playing_sound.stop()
			self.stopped_playing_sound = self.playing_sound
		if self.preview_audio:
			self.preview_audio.stop()
			self.preview_audio = SoundLoader.load(sound)
			self.preview_audio.play()
			self.preview_audio_source = sound
		else:
			self.preview_audio = SoundLoader.load(sound)
			self.preview_audio.play()
			self.preview_audio_source = sound
		self.preview_audio_cache()
	def preview_audio_pause(self,sound):
		if self.preview_audio:
			self.preview_audio.stop()
		if self.stopped_playing_sound:
			time.sleep(.2)
			self.stopped_playing_sound.play()
			self.stopped_playing_sound = None
	def preview_audio_cache(self):
		for i in self.played_preview_audio:
			if self.preview_audio and self.preview_audio_source == i[1] and self.preview_audio.state== 'stop':
				i[0].icon = 'play'
			elif self.preview_audio and self.preview_audio_source == i[1]:
				i[0].icon = 'pause'
			else:
				i[0].icon = 'play'
		self.played_preview_audio.clear()
	def scroll_direction(self, new_scroll_pos_y, scroll_y, refresh_callback, root_layout):
		if new_scroll_pos_y - self.scroll_pos_y<0:
			#print('up')
			pass
		else:
			pass
			#print('down')
		if self.scroll_pos_y - new_scroll_pos_y > dp(40) and scroll_y == 1:
			if self.refreshed == False:
				print('refresh')
				self.refreshed = True
				self.home_buffer = False
				self.home_index=0
				self.refresh_spinner = RefreshSpinner(_refresh_layout=root_layout)
				root_layout.add_widget(self.refresh_spinner)
				self.refresh_spinner.start_anim_spinner()
				refresh_callback()
		if self.root_screen.current == 'home_screen':
			if (scroll_y*self.home_page.ids.recycle_layout.height) < (2*self.window.height) and new_scroll_pos_y - self.scroll_pos_y > dp(5):
				if self.home_buffer == False:
					print('buffering')
					self.home_buffer = True
					self.home_index+=1
					action = threading.Thread(target = self.home_posts_buffer)
					action.start()
			if new_scroll_pos_y - self.scroll_pos_y > dp(25) and scroll_y == 0:
				print('end')
				'''if self.home_buffer == False:
					self.home_buffer = True
					self.home_index+=1
					action = threading.Thread(target = self.home_posts_buffer)
					action.start()'''
		self.scroll_pos_y = new_scroll_pos_y
	def home_posts_buffer(self):
		Clock.schedule_once(self.load_home_posts, 0)
	def load_home_posts(self,instance):
		running_app.display_posts(running_app.user)
	def buffer_done(self):
		print('buffer_done')
		Clock.schedule_once(self.buffer_reset, 3)
	def buffer_reset(self,instance):
		self.home_buffer = False
	def refresh_callback (self):
		print('refreshing.....')
		# stop all functions such as video playing
		self.video_cache()
		Clock.schedule_once(self.display_posts, 3)
	def refresh_done(self):
		print('hide spinner')
		self.refresh_spinner.hide_anim_spinner()
		self.refreshed = False
	def double_scroll_update(self,new_scroll_pos_y,inner_scroll,inner_scroll_layout,outer_scroll,outer_scroll_layout):
		if new_scroll_pos_y - inner_scroll.scroll_pos_y<0:
			pass
		else:
			if outer_scroll.scroll_y >0:
				scroll_distance = (inner_scroll.scroll_pos_y - new_scroll_pos_y)/outer_scroll_layout.height
				inner_scroll.scroll_y = inner_scroll.static_scroll_y
				outer_scroll.scroll_y+=scroll_distance
	def search_pics(self):
		paths = [['screenshots/home',self.home_screenimg],['screenshots/challenges',self.challenge_screenimg],['screenshots/my galaxy',self.my_galaxyimg],['screenshots/notifications',self.notifications_screenimg]]
		for i in paths:
			for r,d,f in os.walk(i[0]):
				for file in f:
					if file.endswith(".png"):
						i[1].append(os.path.join(r,file))
					elif file.endswith(".jpg"):
						i[1].append(os.path.join(r,file))
	def like_post(self, info,root_post):
		check_like_sql = "SELECT * FROM `likes` WHERE Userid = %s AND post_id = %s"
		like_post_sql = "INSERT INTO `likes`(`Userid`, `post_id`) VALUES (%s,%s)"
		delete_like_sql = "DELETE FROM `likes` WHERE Userid = %s AND post_id = %s"
		values =(self.user,info[2])
		try:
			self.dbconnection()
			self.mycursor.execute(check_like_sql, values)
			result = self.mycursor.fetchone()
			if result == None:
				self.mycursor.execute(like_post_sql, values)
				if root_post:
					root_post.likes+=1
			else:
				self.mycursor.execute(delete_like_sql, values)
				if root_post:
					root_post.likes-=1
			self.mydb.commit()
		except Exception as e:
			print(e)
			# return the icon to previous color
	def likes(self,info):
		print(info)
		likes_screen = LikeScreen()
		self.video_cache()
		for i in self.root_screen.current_screen.ids.screen_manager.screens:
			if i.name == 'likes_screen':
				self.root_screen.current_screen.ids.screen_manager.remove_widget(i)
		self.root_screen.current_screen.ids.screen_manager.transition = NoTransition()
		self.root_screen.current_screen.ids.screen_manager.add_widget(likes_screen)
		self.root_screen.current_screen.ids.screen_manager.current= 'likes_screen'
		search_like_sql = "SELECT users.Userid,users.Username,users.ProfilePicture FROM `users` INNER JOIN `likes` ON likes.Userid = users.Userid WHERE likes.post_id = %s OR likes.Userid = %s ORDER BY likes.id DESC LIMIT 30 OFFSET 0"
		like_values = [info[2],info[2]]
		self.dbconnection()
		self.mycursor.execute(search_like_sql, like_values)
		like_result = self.mycursor.fetchall()
		for i in like_result:
			likes_list=LikesCard()
			check_pin_sql = "SELECT * FROM `pins` WHERE Userid = %s AND pinned_id = %s"
			if i[0]!= self.user:
				self.mycursor.execute(check_pin_sql, [self.user,i[0]])
				pin_result = self.mycursor.fetchone()
				if pin_result == None:
					likes_list.pinned = False
				else:
					likes_list.pinned = True
			likes_list.user_info = i
			likes_list.ids.username.text = i[1]
			likes_list.ids.profile_pic.source = i[2]
			if i[0] == self.user:
				likes_list.ids.like_card_lay.remove_widget(likes_list.ids.pin_icon)
			likes_screen.ids.likes_scroll.add_widget(likes_list)
	def comment_on_post(self,info,comment,layout,root_post):
		print(info)
		print(comment.text)
		send_comment_sql = "INSERT INTO `comments`(`post_id`,`Userid`,`comment`) VALUES (%s,%s,%s)"
		comment_values = [info[2],self.user,comment.text]
		if comment.text != '':
			self.dbconnection()
			self.mycursor.execute(send_comment_sql,comment_values)
			self.mydb.commit()
			comments_list = CommentsCard()
			comments_list.time = 'Now'
			comments_list.ids.comment.text = comment.text
			comments_list.ids.username.text = self.user_info[2]
			comments_list.ids.profile_pic.source = self.profile_pic
			comments_list.user_info = [self.user,self.user_info[2],self.profile_pic,comment.text]
			before = comments_list.ids.comment._label.render()
			comments_list.ids.comment.text_size=((self.window.width - dp(100)), None)
			after = comments_list.ids.comment._label.render()
			comments_list.ids.comment.height = (after[1]/before[1])*before[1]
			comment.text = ''
			layout.add_widget(comments_list)
			if root_post:
				if root_post.likecomment:
					root_post.likecomment.comments+=1
	def comments(self,info,root_post): 
		print(info)
		#if self.comments_screen:
		#	self.comments_screen.dismiss()
		self.video_cache()
		self.comments_screen = CommentScreen()
		self.comments_screen.ids.profile_pic.source = self.profile_pic
		self.comments_screen.info = info
		self.comments_screen.likecomment = root_post
		self.comments_screen.open()
		search_comment_sql = "SELECT users.Userid,users.Username,users.ProfilePicture,comments.comment,comments.time FROM `users` INNER JOIN `comments` ON comments.Userid = users.Userid WHERE comments.post_id = %s OR comments.Userid = %s ORDER BY comments.id ASC LIMIT 30 OFFSET 0"
		comment_values = [info[2],info[2]]
		self.dbconnection()
		self.mycursor.execute(search_comment_sql, comment_values)
		comment_result = self.mycursor.fetchall()
		self.comments_screen.ids.comments_scroll.clear_widgets()
		comments = []
		if info[3]!='':
			self_comment = [info[1],info[6],info[7],info[3]]
			comments.append(self_comment)
		for i in comment_result:
			comments.append(i)
		for i in comments:
			print(i)
			comments_list = CommentsCard()
			check_pin_sql = "SELECT * FROM `pins` WHERE Userid = %s AND pinned_id = %s"
			if i[0]!= self.user:
				self.mycursor.execute(check_pin_sql, [self.user,i[0]])
				pin_result = self.mycursor.fetchone()
				if pin_result == None:
					comments_list.pinned = False
				else:
					comments_list.pinned = True
			comments_list.ids.comment.text = i[3]
			comments_list.ids.username.text = i[1]
			comments_list.ids.profile_pic.source = i[2]
			comments_list.user_info = i
			before = comments_list.ids.comment._label.render()
			comments_list.ids.comment.text_size=((self.window.width - dp(100)), None)
			after = comments_list.ids.comment._label.render()
			comments_list.ids.comment.height = (after[1]/before[1])*before[1]
			try:
				posted_time = i[4]
				diff = post_timestamp(posted_time)
				comments_list.time = str(diff)
			except:
				pass
			self.comments_screen.ids.comments_scroll.add_widget(comments_list)
	def repost(self, info):
		if info[1]!= self.user:
			check_repost_sql = "SELECT * FROM `reposts` WHERE Userid = %s AND post_id = %s"
			repost_post_sql = "INSERT INTO `reposts`(`Userid`, `post_id`) VALUES (%s,%s)"
			delete_repost_sql = "DELETE FROM `reposts` WHERE Userid = %s AND post_id = %s"
			values =(self.user,info[2])
			try:
				self.dbconnection()
				self.mycursor.execute(check_repost_sql, values)
				result = self.mycursor.fetchone()
				if result == None:
					self.mycursor.execute(repost_post_sql, values)
				else:
					print(result)
					self.mycursor.execute(delete_repost_sql, values)
				self.mydb.commit()
			except Exception as e:
				raise e
	def save_post(self, info):
		if info[1]!= self.user:
			check_save_sql = "SELECT * FROM `post_saves` WHERE Userid = %s AND post_id = %s"
			save_post_sql = "INSERT INTO `post_saves`(`Userid`, `post_id`) VALUES (%s,%s)"
			delete_save_sql = "DELETE FROM `post_saves` WHERE Userid = %s AND post_id = %s"
			values =(self.user,info[2])
			try:
				self.dbconnection()
				self.mycursor.execute(check_save_sql, values)
				result = self.mycursor.fetchone()
				if result == None:
					self.mycursor.execute(save_post_sql, values)
				else:
					print(result)
					self.mycursor.execute(delete_save_sql, values)
				self.mydb.commit()
			except Exception as e:
				raise e
	def post_options(self,info,root_post):
		self.video_cache()
		if info[1]==self.user:
			options = SelfPostOptions(post_info = info,root_post = root_post)
		else:
			if info[1] in self.live_pinned_users:
				root_post.pinned = True
			elif info[1] in self.live_unpinned_users:
				root_post.pinned = False
			options = PostOptions(post_info = info,root_post = root_post)
		options.open()
	def delete_post_prompt(self,info,root_post):
		if info[1] == self.user:
			post_warning_dialog = ConfirmationPopup(
				message="Are you sure you want to delete this post.",
				callback=self.delete_post,
				parameters = [info,root_post])
			post_warning_dialog.open()
		else:

			toast("Sorry you can't delete this post")
	def delete_post(self,args,info_list,layout):
		layout.dismiss()
		if args== 'Confirm':
			toast('Please Wait ...')#The resulting code is to be performed by a sync
			info = info_list[0]
			root_post = info_list[1]
			delete_sqls = []
			delete_post_likes_sql = "DELETE FROM `likes` WHERE post_id = %s OR post_id = %s"
			delete_sqls.append(delete_post_likes_sql)
			delete_post_comments_sql = "DELETE FROM `comments` WHERE post_id = %s OR post_id = %s"
			delete_sqls.append(delete_post_comments_sql)
			delete_post_saves_sql = "DELETE FROM `post_saves` WHERE post_id = %s OR post_id = %s"
			delete_sqls.append(delete_post_saves_sql)
			delete_post_reposts_sql = "DELETE FROM `reposts` WHERE post_id = %s OR post_id = %s"
			delete_sqls.append(delete_post_reposts_sql)
			delete_post_tags_sql = "DELETE FROM `tags` WHERE post_id = %s OR post_id = %s"
			delete_sqls.append(delete_post_tags_sql)
			delete_post_sql = "DELETE FROM `posts` WHERE post_id = %s OR post_id = %s"
			delete_sqls.append(delete_post_sql)
			if info[4] == 'Image':
				delete_post_media_sql = "DELETE FROM `post_images` WHERE post_id = %s OR post_id = %s"
				delete_sqls.append(delete_post_media_sql)
			elif info[4] == 'Audio':
				delete_post_media_sql = "DELETE FROM `post_audio` WHERE post_id = %s OR post_id = %s"
				delete_sqls.append(delete_post_media_sql)
			elif info[4] == 'Video':
				delete_post_media_sql = "DELETE FROM `post_video` WHERE post_id = %s OR post_id = %s"
				delete_sqls.append(delete_post_media_sql)
			try:
				self.dbconnection()
				for i in delete_sqls:
					self.mycursor.execute(i,[info[2],info[2]])
				self.mydb.commit()
			except Exception as e:
				print(e)
				toast('Check Your Internet Connection')
			else:
				rp_parent = root_post.parent
				root_post.parent.remove_widget(root_post)
				self.adjust_scroll([rp_parent,(-1*root_post.height)])
		else:
			pass
	def pin_user(self, info,root_post):
		check_pin_sql = "SELECT * FROM `pins` WHERE Userid = %s AND pinned_id = %s"
		pin_user_sql = "INSERT INTO `pins`(`Userid`, `pinned_id`) VALUES (%s,%s)"
		delete_pin_sql = "DELETE FROM `pins` WHERE Userid = %s AND pinned_id = %s"
		values =(self.user,info)
		try:
			self.dbconnection()
			self.mycursor.execute(check_pin_sql, values)
			result = self.mycursor.fetchone()
			if result == None:
				self.mycursor.execute(pin_user_sql, values)
				self.live_pinned_users.append(info)
				if info in self.live_unpinned_users:
					self.live_unpinned_users.remove(info)
				root_post.pinned = True
			else:
				self.mycursor.execute(delete_pin_sql, values)
				self.live_unpinned_users.append(info)
				if info in self.live_pinned_users:
					self.live_pinned_users.remove(info)
				root_post.pinned = False
			self.mydb.commit()
		except Exception as e:
			print(e)
	def pins(self,info,mode):
		print(info)
		pins_screen = PinsScreen()
		pins_screen.title = mode
		pins_screen.profile_pic = info[1]
		self.video_cache()
		for i in self.root_screen.current_screen.ids.screen_manager.screens:
			if i.name == 'pins_screen':
				self.root_screen.current_screen.ids.screen_manager.remove_widget(i)
		self.root_screen.current_screen.ids.screen_manager.transition = NoTransition()
		self.root_screen.current_screen.ids.screen_manager.add_widget(pins_screen)
		self.root_screen.current_screen.ids.screen_manager.current= 'pins_screen'
		if mode == 'Pins':
			search_pins_sql = "SELECT users.Userid,users.Username,users.ProfilePicture FROM `users` INNER JOIN `pins` ON pins.Userid = users.Userid WHERE pins.pinned_id = %s OR pins.pinned_id = %s ORDER BY pins.id DESC LIMIT 30 OFFSET 0"
		else:
			search_pins_sql = "SELECT users.Userid,users.Username,users.ProfilePicture FROM `users` INNER JOIN `pins` ON pins.pinned_id = users.Userid WHERE pins.Userid = %s OR pins.Userid = %s ORDER BY pins.id DESC LIMIT 30 OFFSET 0"
		pins_values = [info[0],info[0]]
		self.dbconnection()
		self.mycursor.execute(search_pins_sql, pins_values)
		pins_result = self.mycursor.fetchall()
		for i in pins_result:
			pins_list=LikesCard()
			check_pin_sql = "SELECT * FROM `pins` WHERE Userid = %s AND pinned_id = %s"
			if i[0]!= self.user:
				self.mycursor.execute(check_pin_sql, [self.user,i[0]])
				pin_result = self.mycursor.fetchone()
				if pin_result == None:
					pins_list.pinned = False
				else:
					pins_list.pinned = True
			pins_list.user_info = i
			pins_list.ids.username.text = i[1]
			pins_list.ids.profile_pic.source = i[2]
			if i[0] == self.user:
				pins_list.ids.like_card_lay.remove_widget(pins_list.ids.pin_icon)
			pins_screen.ids.pins_scroll.add_widget(pins_list)
	def block_user(self,info,root_post):
		check_block_sql = "SELECT * FROM `blocked_users` WHERE Userid = %s AND blocked_user = %s"
		block_user_sql = "INSERT INTO `blocked_users`(`Userid`, `blocked_user`) VALUES (%s,%s)"
		delete_block_sql = "DELETE FROM `blocked_users` WHERE Userid = %s AND blocked_user = %s"
		values =(self.user,info)
		try:
			self.dbconnection()
			self.mycursor.execute(check_block_sql, values)
			result = self.mycursor.fetchone()
			if result == None:
				self.mycursor.execute(block_user_sql, values)
				self.live_blocked_users.append(info)
				if info in self.live_unblocked_users:
					self.live_unblocked_users.remove(info)
				root_post.blocked = True
			else:
				self.mycursor.execute(delete_block_sql, values)
				self.live_unblocked_users.append(info)
				if info in self.live_blocked_users:
					self.live_blocked_users.remove(info)
				root_post.blocked = False
			self.mydb.commit()
		except Exception as e:
			print(e)
	def profile(self,info,root_post):
		if info[0] == self.user:
			print('Current User')
		else:
			self.other_profile = ProfileScreen()
			for i in self.root_screen.current_screen.ids.screen_manager.screens:
				if i.name == 'profile_screen':
					self.root_screen.current_screen.ids.screen_manager.remove_widget(i)
			self.root_screen.current_screen.ids.screen_manager.transition = NoTransition()
			try:
				self.root_screen.current_screen.ids.screen_manager.remove_widget(self.other_profile)
			except:
				pass
			self.other_profile.info = info
			self.other_profile.user = info[0]
			self.other_profile.username = info[1]
			self.other_profile.profile_pic = info[2]
			self.root_screen.current_screen.ids.screen_manager.add_widget(self.other_profile)
			self.video_cache()
			self.root_screen.current_screen.ids.screen_manager.current = 'profile_screen'
			if root_post:
				if root_post.pinned:
					self.other_profile.pinned = True
				else:
					self.other_profile.pinned = False
			if info[0] in self.live_pinned_users:
				self.other_profile.pinned = True
			elif info[0] in self.live_unpinned_users:
				self.other_profile.pinned = False
	def messages(self):
		self.root_manager.transition = SlideTransition()
		self.video_cache()
		self.root_manager.transition.direction = 'left'
		self.root_manager.current = 'messages_screen'
		for i in range(17):
			messages_list = MessagesCard()
			self.messages_screen.ids.messages_scroll.add_widget(messages_list)
	def messaging(self):
		self.messaging_screen = MessagingScreen()
		self.video_cache()
		self.messaging_screen.ids.profile_pic.source = self.profile_pic
		self.root_manager.add_widget(self.messaging_screen)
		self.root_manager.transition = NoTransition()
		self.root_manager.current = 'messaging_screen'
		layout = BoxLayout(orientation = 'vertical', spacing = dp(10), padding = dp(5) ,size_hint=(1, None))
		layout.bind(minimum_height=layout.setter('height'))
		action = 'receive'
		for i in range(1,20):
			l = Label(halign = 'left',text='Text ' * (i*3), markup = True, color = [0,0,0,1],text_size=(None, None), size_hint_y=None,pos_hint = {'center_x':.5, 'center_y':.5})
			# calculating height here
			before = l._label.render()
			l.text_size=(self.window.width*0.8, None)
			after = l._label.render()
			l.height = (after[1]/before[1])*before[1] # ammount of rows * single row height
			# end
			w = self.window.width*0.8
			print(before)
			print(l.height)
			if before[0]< self.window.width*0.8:
				w = before[0]
				l.text_size=(before[0], None)
			if action == 'receive':
				pos = {'left' :1}
			else:
				pos = {'right' :1}
			r = BoxLayout(orientation = 'vertical', size_hint = (1,1))
			b = MessageLabel(size_hint_y=None,size_hint_x=None, width= w+10, padding = 5,height = l.height+ 20, pos_hint = pos)
			a_l = BoxLayout()
			t = Label(text = 'Time', halign = 'right', size_hint_x = 1,markup = True, color = [.05,.05,.05,1], font_size = 10,text_size=(None, None),pos_hint = {'center_y':.5})
			r.add_widget(l)
			a_l.add_widget(Widget())
			a_l.add_widget(t)
			r.add_widget(a_l)
			b.add_widget(r)
			layout.add_widget(b)
			if action == 'receive':
				action = 'send'
				b.color = [1,1,1,1]
			else:
				action = 'receive'
				b.color = [1,.95,.9,.75]
		self.messaging_screen.ids.messaging_scroll.add_widget(layout)
	def build_galaxy(self):
		pass
	def display_galaxy_posts(self):
		galaxy_collection_sql = "SELECT posts.post_id,post_images.image FROM `posts` INNER JOIN `post_images` ON posts.post_id = post_images.post_id WHERE posts.type = 'Image' AND post_images.image_name = CONCAT (posts.post_id,'/Image1') ORDER BY posts.id DESC LIMIT %s OFFSET %s"
		self.dbconnection()
		self.mycursor.execute(galaxy_collection_sql,[9,0])
		collection_result = self.mycursor.fetchall()
		galaxy_collection = MyGalaxyGallery(collection = collection_result)
		self.my_galaxy.ids.my_galaxy_layout.add_widget(galaxy_collection)
		galaxy_discover_people_sql = "SELECT Userid,Username,ProfilePicture FROM `users`"
		galaxy_people_post_sql = "SELECT posts.post_id, post_images.image FROM `users` INNER JOIN `posts` INNER JOIN `post_images` ON users.Userid = posts.Userid AND posts.post_id = post_images.post_id WHERE users.Userid = %s OR users.Userid = %s ORDER BY posts.id DESC"
		self.mycursor.execute(galaxy_discover_people_sql)
		discover_people_result = self.mycursor.fetchall()
		people_layout = PeopleLayout(title = 'Discover People')
		count = 0
		for i in discover_people_result:
			self.dbconnection()
			self.mycursor.execute(galaxy_people_post_sql,[i[0],i[0]])
			people_post_result = self.mycursor.fetchone()
			check_pin_sql = "SELECT * FROM `pins` WHERE pinned_id = %s AND Userid = %s"
			if i[0]!= self.user:
				self.dbconnection()
				self.mycursor.execute(check_pin_sql,(i[0],self.user))
				pin_result = self.mycursor.fetchone()
				if count == 0:
					people_box = BoxLayout(size_hint = (1,1), spacing = dp(10), padding = dp(5), pos_hint ={'center_x':.5,'top':1})
					people_card = PeopleCard(pos_hint = {'center_x':.5,'top':1},username = i[1],info = i)
					people_box.add_widget(people_card)
					people_layout.ids.people_carousel.add_widget(people_box)
					count+=1
				else:
					people_card = PeopleCard(pos_hint = {'center_x':.5,'top':1},username = i[1],info = i)
					people_box.add_widget(people_card)
					count = 0
				if i[2]!='':
					people_card.profile_pic = i[2]
				if people_post_result:
					people_card.cover_image = people_post_result[1]

				if pin_result == None:
					people_card.pinned = False
				else:
					people_card.pinned = True
		self.my_galaxy.ids.my_galaxy_layout.add_widget(people_layout)
		#galaxy_photos_sql = "SELECT post_images.image,posts.post_id,users.Userid,users.Username,users.ProfilePicture FROM `post_images` INNER JOIN `posts` INNER JOIN `users` ON post_images.post_id = posts.post_id AND posts.Userid = users.Userid WHERE posts.type = 'Image' AND post_images.image_name = CONCAT (posts.post_id,'/Image1') "
		#galaxy_photos_sql = "SELECT post_images.post_id,posts.post_id FROM `post_images` INNER JOIN `posts` "
		self.dbconnection()
		galaxy_photos_sql =  "SELECT posts.post_id,users.Userid,post_images.image,users.Username,users.ProfilePicture,posts.caption FROM `post_images` INNER JOIN `posts` INNER JOIN `users` ON post_images.post_id = posts.post_id AND posts.Userid = users.Userid WHERE posts.type = 'Image' AND post_images.image_name = CONCAT (posts.post_id,'/Image1') ORDER BY posts.id DESC LIMIT 10 OFFSET 0"
		self.mycursor.execute(galaxy_photos_sql)
		galaxy_photos = self.mycursor.fetchall()
		post_display = MyGalaxyPostDisplay()
		for i in galaxy_photos:
			sub_info = self.check_sub_info([i[3],i[1],i[0]])
			post_display_unit = MyGalaxyPostDisplayUnit(info = i,sub_info = sub_info,pinned = sub_info[5])
			if i[1]==self.user:
				post_display_unit.ids.pin_icon.parent.remove_widget(post_display_unit.ids.pin_icon)
				post_display_unit.ids.repost_icon.parent.remove_widget(post_display_unit.ids.repost_icon)
				post_display_unit.ids.save_icon.parent.remove_widget(post_display_unit.ids.save_icon)
			post_display.ids.photos_carousel.add_widget(post_display_unit)
		self.my_galaxy.ids.my_galaxy_layout.add_widget(post_display)
		'''
			if myresult != []:
				interval_object = PeopleLayout(title = 'Discover People')
				interval_layout = BoxLayout(orientation = 'vertical',size_hint = (None,None),size = (self.window.width,interval_object.height))
				interval_layout.add_widget(FullSeparator(pos_hint = {'top':1}))
				interval_layout.add_widget(interval_object)
				interval_layout.add_widget(FullSeparator(pos_hint = {'bottom':1}))
				print(interval_layout.height)
				print(interval_object.height)
				self.home_page.ids.recycle_layout.add_widget(interval_layout)
				self.displaying_posts_list[1]+=(interval_object.height+dp(18))
				'''
		self.dbconnection()
		galaxy_videos_sql =  "SELECT posts.post_id,users.Userid,post_video.video,post_video.thumbnail,posts.image_ratio,users.Username,users.ProfilePicture,posts.caption FROM `post_video` INNER JOIN `posts` INNER JOIN `users` ON post_video.post_id = posts.post_id AND posts.Userid = users.Userid WHERE posts.type = 'Video' ORDER BY posts.id DESC LIMIT 10 OFFSET 0"
		self.mycursor.execute(galaxy_videos_sql)
		galaxy_videos = self.mycursor.fetchall()
		video_display = MyGalaxyVideos()
		bcarousel = video_display.ids.carousel
		bcarousel.clear_widgets()
		num = 0
		for i in galaxy_videos:
			sub_info = self.check_sub_info([i[5],i[1],i[0]])
			vid = VideoDisplayUnit(thumbnail = i[3],source = i[2],num = num,base = bcarousel, scrn = 'trending_screen',info = i,sub_info = sub_info,pinned = sub_info[5])
			bcarousel.add_widget(vid)
			if num == 0:
				bcarousel.height = (self.window.width/i[4]+dp(55))
			num+=1
		self.my_galaxy.ids.my_galaxy_layout.add_widget(video_display)
		galaxy_audio_sql =  "SELECT posts.post_id,users.Userid,post_audio.audio,post_audio.cover_photo,post_audio.title,users.Username,users.ProfilePicture,posts.caption FROM `post_audio` INNER JOIN `posts` INNER JOIN `users` ON post_audio.post_id = posts.post_id AND posts.Userid = users.Userid WHERE posts.type = 'Audio' ORDER BY posts.id DESC LIMIT 10 OFFSET 0"
		self.mycursor.execute(galaxy_audio_sql)
		galaxy_audio = self.mycursor.fetchall()
		sub_info_list = []
		pinned_list = []
		source_list = []
		for i in galaxy_audio:
			source_list.append(i[2])
			sub_info = self.check_sub_info([i[5],i[1],i[0]])
			sub_info_list.append(sub_info)
			pinned_list.append(sub_info[5])
		audio_display = MyGalaxyAudioDisplay(audio = galaxy_audio,sub_info = sub_info_list,pinned = pinned_list,source = source_list)
		self.my_galaxy.ids.my_galaxy_layout.add_widget(audio_display)
		galaxy_tags_sql = "SELECT DISTINCT tag_name from `tags` LIMIT 10"
		self.dbconnection()
		self.mycursor.execute(galaxy_tags_sql)
		galaxy_tags = self.mycursor.fetchall()
		galaxy_tags_posts_sql = "SELECT tags.tag_name,post_images.image FROM `tags` INNER JOIN `posts` INNER JOIN `post_images` ON posts.post_id = tags.post_id AND posts.post_id = post_images.post_id WHERE tags.tag_name = %s AND posts.type = 'Image' ORDER BY posts.id DESC LIMIT 3"
		tags_layout = DiscoverTagsLayout()
		for i in galaxy_tags:
			self.mycursor.execute(galaxy_tags_posts_sql,(i[0],))
			galaxy_tags_posts = self.mycursor.fetchall()
			if len(galaxy_tags_posts)>0:
				tag_pics = []
				for f in range(3):
					try:
						tag_pics.append(galaxy_tags_posts[f][1])
					except Exception as e:
						print(e)
						tag_pics.append('assets/purple.jpg')
				tags_card = DiscoverTagsCard(info = i[0],pics = tag_pics)
				tags_layout.ids.tags_carousel.add_widget(tags_card)
				print(i[0]+' - '+str(galaxy_tags_posts))
		self.my_galaxy.ids.my_galaxy_layout.add_widget(tags_layout)
	def my_galaxy_open_post(self,info):
		self.video_cache()
		print(info)
		image_screen = ImageScreen()
		for i in self.root_screen.current_screen.ids.screen_manager.screens:
			if i.name == 'image_screen':
				self.root_screen.current_screen.ids.screen_manager.remove_widget(i)
		self.root_screen.current_screen.ids.screen_manager.transition = NoTransition()
		self.root_screen.current_screen.ids.screen_manager.add_widget(image_screen)
		self.root_screen.current_screen.ids.screen_manager.current = 'image_screen'
		user_posts_sql = "SELECT posts.id,posts.UserId,posts.post_id,posts.caption,posts.type,posts.image_ratio,users.Username,users.ProfilePicture,posts.emotion,posts.time FROM `posts` INNER JOIN `users` ON posts.Userid = users.Userid WHERE posts.post_id = %s ORDER BY posts.id DESC " #LIMIT 15 OFFSET 0
		try:
			self.dbconnection()
			self.mycursor.execute(user_posts_sql,(info[0],))
			myresult = self.mycursor.fetchone()
			print(myresult)
			image_screen.ids.post_scroll.clear_widgets()
			post_images_sql = "SELECT * FROM `post_images` WHERE `post_id` = %s"
			post_images_values = [info[0],]
			self.mycursor.execute(post_images_sql,post_images_values)
			result = self.mycursor.fetchall()
			sub_info = self.check_sub_info(myresult)
			self.display_a_post(myresult,result,image_screen.ids.post_scroll,sub_info,image_screen.ids.post_scroll)
		except Exception as e:
			print(e)
			toast('Check Your Internet Connection')
	def	my_galaxy_search(self,textinput,layout):
		if textinput.text !=textinput.previous_text and textinput.text!='':
			print(textinput.text)
			textinput.previous_text = textinput.text
			self.dbconnection()
			if len(textinput.text)<3:
				my_galaxy_search_sql = "SELECT Userid,Username,FullName,ProfilePicture,Bio FROM `users` WHERE Username LIKE %s OR FullName LIKE %s"
				self.mycursor.execute(my_galaxy_search_sql,(textinput.text+ "%",textinput.text+ "%"))
				print(my_galaxy_search_sql,(textinput.text+ "%",textinput.text+ "%"))
			elif len(textinput.text)<10:
				my_galaxy_search_sql = "SELECT Userid,Username,FullName,ProfilePicture,Bio FROM `users` WHERE Username LIKE CONCAT('%', %s, '%') OR FullName  LIKE CONCAT('%', %s, '%')"
				self.mycursor.execute(my_galaxy_search_sql,(textinput.text,textinput.text))
			else:
				my_galaxy_search_sql = "SELECT Userid,Username,FullName,ProfilePicture,Bio FROM `users` WHERE Username LIKE CONCAT('%', %s, '%')  OR FullName LIKE CONCAT('%', %s, '%') OR Bio LIKE CONCAT('%', %s, '%')"
				self.mycursor.execute(my_galaxy_search_sql,(textinput.text,textinput.text,textinput.text))
			search_result = self.mycursor.fetchall()
			print(search_result)
			layout.clear_widgets()
			for i in search_result:
				layout.add_widget(SearchCard(info = i))
	def posting(self):
		self.root_manager.transition = FadeTransition()
		self.video_cache()
		self.root_manager.current = 'post_screen'
	def menu(self):
		self.root_manager.transition.direction = 'left'
		self.video_cache()
		self.root_manager.current = 'menu_screen'
		print(self.root_screen.current_screen)
	def open_search_screen(self):
		self.root_screen.current_screen.ids.screen_manager.transition = CardTransition()
		self.search_screen=SearchScreen()
		self.root_screen.current_screen.ids.screen_manager.add_widget(self.search_screen)
		self.video_cache()
		self.root_screen.current_screen.ids.screen_manager.current = 'search_screen'
	def artificial_scroll(self,new_scroll_pos_y,scroll,layout):
		pass
		'''v_scroll_dis = new_scroll_pos_y - self.scroll_pos_y
		self.scroll_pos_y = new_scroll_pos_y
		print(v_scroll_dis)
		r_scroll_dis = v_scroll_dis/layout.height
		scroll_y = scroll.scroll_y - r_scroll_dis
		if v_scroll_dis<0.5 or v_scroll_dis>0.5:
			if scroll_y < 0:
				scroll.scroll_y = 0
			elif scroll_y >1:
				scroll.scroll_y = 1
			else:
				scroll.scroll_y = scroll_y'''
	def change_color(self, a, b, c):
		a.text_color=[0,0,0,1]
		b.text_color=[0,0,0,1]
		c.text_color=[0,0,0,1]
	def open_camera(self):
		toast('Open Camera')
	def challenge_definition(self):
		challenge_definition = ChallengeDefinition()
		self.root_screen.current_screen.ids.screen_manager.transition = NoTransition()
		self.root_screen.current_screen.ids.screen_manager.add_widget(challenge_definition)
		self.root_screen.current_screen.ids.screen_manager.current = 'challenge_definition'
		self.video_cache()
		before = challenge_definition.ids.description._label.render()
		challenge_definition.ids.description.text_size=((self.window.width - dp(70)), None)
		after = challenge_definition.ids.description._label.render()
		challenge_definition.ids.description.height = (after[1]/before[1])*before[1]
	def display_tag_posts(self,tag_name,layout,screen):
		print(tag_name)
		self.video_cache()
		initial = screen.manager.height
		user_reposts_sql = "SELECT posts.id,posts.UserId,posts.post_id,posts.caption,posts.type,posts.image_ratio,users.Username,users.ProfilePicture,posts.emotion,posts.time FROM `tags` INNER JOIN `posts` INNER JOIN `users` ON posts.post_id = tags.post_id AND posts.UserId = users.UserId WHERE tags.tag_name = %s OR tags.tag_name = %s ORDER BY posts.id DESC LIMIT 10" #LIMIT 15 OFFSET 0
		try:
			self.dbconnection()
			self.mycursor.execute(user_reposts_sql,[tag_name,tag_name])
			myresult = self.mycursor.fetchall()
			layout.clear_widgets()
			displaying_posts_list = [layout,0]
			num = 0
			for i in myresult:
				if i[4] == 'Image':
					post_images_sql = "SELECT * FROM `post_images` WHERE `post_id` = %s OR `id`= %s"
					post_images_values = [i[2],i[2]]
					self.mycursor.execute(post_images_sql,post_images_values)
					result = self.mycursor.fetchall()
					if len(result) == 1:
						image = FitImageTouch(pos_hint = {'top':1},source = result[0][2],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					else:
						image = FitMultipleImageTouch(pos_hint = {'top':1},source = result[0][2],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					layout.add_widget(image)
				elif i[4] == 'Audio':
					post_audio_sql = "SELECT * FROM `post_audio` WHERE `post_id` = %s OR `id`= %s"
					post_audio_values = [i[2],i[2]]
					self.mycursor.execute(post_audio_sql,post_audio_values)
					result = self.mycursor.fetchone()
					image = FitAudioTouch(pos_hint = {'top':1},source = result[6],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					layout.add_widget(image)
				elif i[4] == 'Video':
					post_video_sql = "SELECT * FROM `post_video` WHERE `post_id` = %s OR `id`= %s"
					post_video_values = [i[2],i[2]]
					self.mycursor.execute(post_video_sql,post_video_values)
					result = self.mycursor.fetchone()
					image = FitVideoTouch(pos_hint = {'top':1},source = result[4],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					layout.add_widget(image)
				if num == 0 or num % 3 == 0:
					displaying_posts_list[1]+=image.height
				num+=1
		except Exception as e:
			print(e)
			toast('Check your Internet Connection')
	def display_user_posts(self,user,layout,screen):
		self.video_cache()
		user_posts_sql = "SELECT posts.id,posts.UserId,posts.post_id,posts.caption,posts.type,posts.image_ratio,users.Username,users.ProfilePicture,posts.emotion,posts.time FROM `posts` INNER JOIN `users` ON posts.Userid = users.Userid WHERE users.UserId = %s ORDER BY posts.id DESC "%user #LIMIT 15 OFFSET 0
		try:
			self.dbconnection()
			self.mycursor.execute(user_posts_sql)
			myresult = self.mycursor.fetchall()
			layout.clear_widgets()
			for i in myresult:
				if i[4] == 'Image':
					post_images_sql = "SELECT * FROM `post_images` WHERE `post_id` = %s OR `id`= %s"
					post_images_values = [i[2],i[2]]
					self.mycursor.execute(post_images_sql,post_images_values)
					result = self.mycursor.fetchall()
					if len(result) == 1:
						image = FitImageTouch(pos_hint = {'top':1},source = result[0][2],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
						layout.add_widget(image)
					else:
						image = FitMultipleImageTouch(pos_hint = {'top':1},source = result[0][2],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
						layout.add_widget(image)
				elif i[4] == 'Audio':
					post_audio_sql = "SELECT * FROM `post_audio` WHERE `post_id` = %s OR `id`= %s"
					post_audio_values = [i[2],i[2]]
					self.mycursor.execute(post_audio_sql,post_audio_values)
					result = self.mycursor.fetchone()
					image = FitAudioTouch(pos_hint = {'top':1},source = result[6],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					layout.add_widget(image)
				elif i[4] == 'Video':
					post_video_sql = "SELECT * FROM `post_video` WHERE `post_id` = %s OR `id`= %s"
					post_video_values = [i[2],i[2]]
					self.mycursor.execute(post_video_sql,post_video_values)
					result = self.mycursor.fetchone()
					image = FitVideoTouch(pos_hint = {'top':1},source = result[4],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					layout.add_widget(image)
		except Exception as e:
			print(e)
			toast('Check your Internet Connection')	
	def display_user_reposts(self,user,layout,outer_layout,screen):
		self.video_cache()
		initial = screen.manager.height
		user_reposts_sql = "SELECT posts.id,posts.UserId,posts.post_id,posts.caption,posts.type,posts.image_ratio,users.Username,users.ProfilePicture,posts.emotion,posts.time FROM `reposts` INNER JOIN `posts` INNER JOIN `users` ON posts.post_id = reposts.post_id AND posts.UserId = users.UserId WHERE reposts.UserId = %s ORDER BY posts.id DESC LIMIT 10"%user #LIMIT 15 OFFSET 0
		try:
			self.dbconnection()
			self.mycursor.execute(user_reposts_sql)
			myresult = self.mycursor.fetchall()
			layout.clear_widgets()
			displaying_posts_list = [outer_layout,0]
			num = 0
			for i in myresult:
				if i[4] == 'Image':
					post_images_sql = "SELECT * FROM `post_images` WHERE `post_id` = %s OR `id`= %s"
					post_images_values = [i[2],i[2]]
					self.mycursor.execute(post_images_sql,post_images_values)
					result = self.mycursor.fetchall()
					if len(result) == 1:
						image = FitImageTouch(pos_hint = {'top':1},source = result[0][2],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					else:
						image = FitMultipleImageTouch(pos_hint = {'top':1},source = result[0][2],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					layout.add_widget(image)
				elif i[4] == 'Audio':
					post_audio_sql = "SELECT * FROM `post_audio` WHERE `post_id` = %s OR `id`= %s"
					post_audio_values = [i[2],i[2]]
					self.mycursor.execute(post_audio_sql,post_audio_values)
					result = self.mycursor.fetchone()
					image = FitAudioTouch(pos_hint = {'top':1},source = result[6],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					layout.add_widget(image)
				elif i[4] == 'Video':
					post_video_sql = "SELECT * FROM `post_video` WHERE `post_id` = %s OR `id`= %s"
					post_video_values = [i[2],i[2]]
					self.mycursor.execute(post_video_sql,post_video_values)
					result = self.mycursor.fetchone()
					image = FitVideoTouch(pos_hint = {'top':1},source = result[4],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					layout.add_widget(image)
				if num == 0 or num % 3 == 0:
					displaying_posts_list[1]+=image.height
				num+=1
		except Exception as e:
			print(e)
			toast('Check your Internet Connection')
			
		else:
			if displaying_posts_list[1]<initial:
				pass
			else:
				screen.height = displaying_posts_list[1]
				screen.manager.height = displaying_posts_list[1]
				screen.manager.parent.height = displaying_posts_list[1]
				print(str(displaying_posts_list[1]-initial)+'adding height')
				self.adjust_scroll([outer_layout,(displaying_posts_list[1]-initial)])
	def display_user_saved_posts(self,user,layout,outer_layout,screen):
		self.video_cache()
		initial = screen.manager.height
		user_saved_sql = "SELECT posts.id,posts.UserId,posts.post_id,posts.caption,posts.type,posts.image_ratio,users.Username,users.ProfilePicture,posts.emotion,posts.time FROM `post_saves` INNER JOIN `posts` INNER JOIN `users` ON posts.post_id = post_saves.post_id AND posts.UserId = users.UserId WHERE post_saves.UserId = %s ORDER BY posts.id DESC LIMIT 10"%user #LIMIT 15 OFFSET 0
		try:
			self.dbconnection()
			self.mycursor.execute(user_saved_sql)
			myresult = self.mycursor.fetchall()
			layout.clear_widgets()
			displaying_posts_list = [outer_layout,0]
			num = 0
			for i in myresult:
				if i[4] == 'Image':
					post_images_sql = "SELECT * FROM `post_images` WHERE `post_id` = %s OR `id`= %s"
					post_images_values = [i[2],i[2]]
					self.mycursor.execute(post_images_sql,post_images_values)
					result = self.mycursor.fetchall()
					if len(result) == 1:
						image = FitImageTouch(pos_hint = {'top':1},source = result[0][2],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					else:
						image = FitMultipleImageTouch(pos_hint = {'top':1},source = result[0][2],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					layout.add_widget(image)
				elif i[4] == 'Audio':
					post_audio_sql = "SELECT * FROM `post_audio` WHERE `post_id` = %s OR `id`= %s"
					post_audio_values = [i[2],i[2]]
					self.mycursor.execute(post_audio_sql,post_audio_values)
					result = self.mycursor.fetchone()
					image = FitAudioTouch(pos_hint = {'top':1},source = result[6],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					layout.add_widget(image)
				elif i[4] == 'Video':
					post_video_sql = "SELECT * FROM `post_video` WHERE `post_id` = %s OR `id`= %s"
					post_video_values = [i[2],i[2]]
					self.mycursor.execute(post_video_sql,post_video_values)
					result = self.mycursor.fetchone()
					image = FitVideoTouch(pos_hint = {'top':1},source = result[4],size_hint = (None,None),size = (((self.window.width-dp(2))/3),((self.window.width-dp(2))/3)),press_callback = self.open_post,press_parameter = (i, result))
					layout.add_widget(image)
				if num == 0 or num % 3 == 0:
					displaying_posts_list[1]+=image.height
				num+=1
		except Exception as e:
			print(e)
			toast('Check your Internet Connection')
			
		else:
			if displaying_posts_list[1]<initial:
				pass
			else:
				screen.height = displaying_posts_list[1]
				screen.manager.height = displaying_posts_list[1]
				screen.manager.parent.height = displaying_posts_list[1]
				print(str(displaying_posts_list[1]-initial)+'adding height')
				self.adjust_scroll([outer_layout,(displaying_posts_list[1]-initial)])
	def open_edit_profile(self):
		self.video_cache()
		self.edit_profile_screen = EditProfileScreen()
		self.edit_profile_screen.open()
		if self.user_info == []:
			info = self.backup_user_info
			toast('Check Your Internet Connection')
		else:
			info = self.user_info
		try:
			self.edit_profile_screen.ids.username.text= info[2]
			self.edit_profile_screen.ids.profilepic.source= self.profile_pic
			self.edit_profile_screen.ids.fullname.text= info[1]
			self.edit_profile_screen.ids.bio.text= info[9]
			self.edit_profile_screen.ids.portofolio.text= info[10]
			self.edit_profile_screen.ids.email.text= info[4]
			self.edit_profile_screen.ids.phone.text= info[5]
		except:
			toast('Check Your Internet Connection')
	def edit_profile(self, pic, fullname, username, bio, portofolio,email, phone):
		edit_profile_sql = "UPDATE `users` SET `ProfilePicture` =%s , `FullName` =%s , `Username` =%s , `Bio` =%s ,`Portofolio` =%s , `Email` =%s , `Phone` =%s  WHERE Userid = %s"
		values = [pic,fullname,username, bio, portofolio,email, phone, self.user]
		log_popup = LoginProcess()
		log_popup.ids.log_message.text = "Updating...."
		log_popup.open()
		try:
			self.dbconnection()
			self.mycursor.execute(edit_profile_sql, values)
			self.mydb.commit()
			user_sql = "SELECT * FROM `users` WHERE UserId = %s OR DOR = %s"
			self.dbconnection()
			self.mycursor.execute(user_sql,[self.user,self.user])
			result = self.mycursor.fetchone()
			self.user_info = result
			if self.user_info[8] == '':
				self.profile_pic = self.avatar
			else:
				self.profile_pic = self.user_info[8]
				self.user_post_count = result[11]
		except Exception as e:
			print(e)
			log_popup.ids.log_message.text = "Check your Internet Connection"
			log_popup.ids.log_process_layout.remove_widget(log_popup.ids.log_spinner)
			log_popup.auto_dismiss = True
		else:
			log_popup.dismiss()
			self.edit_profile_screen.dismiss()
	def open_profile_pic_select(self, pic_layout):
		self.gallery_images_single = GalleryImagesSingle()
		self.gallery_images_single.open()
		images = []
		for r,d,f in os.walk("assets/"):
			for file in f:
				if file.endswith(".jpg"):
					images.append(os.path.join(r,file))
				elif file.endswith(".JPG"):
					images.append(os.path.join(r,file))
		for i in images:
			image = FitImageTouch(source =i,size_hint = (1,None),press_callback = self.set_profile_pic)
			image.height = (self.window.width/3)-dp(8)
			image.press_parameter = [image,pic_layout,self.gallery_images_single]
			self.gallery_images_single.ids.gallery_scroll.add_widget(image)
	def set_profile_pic(self,parameters):
		parameters[1].source = parameters[0].source
		parameters[2].dismiss()
	def dismiss_edit_profile_screen(self,info,popup):
		if self.user_info == []:
			i = self.backup_user_info
		else:
			i = self.user_info
		if [i[8], i[1], i[2], i[9], i[10],i[4], i[5]] == info:
			popup.dismiss()
		else:
			global pop
			pop = popup
			post_warning_dialog = WarningPopup(
				message="Your saved changes will be lost.",
				callback=self.edit_profile_dialog_callback)
			post_warning_dialog.open()
	def edit_profile_dialog_callback(self,args):
		global pop 
		if args=='Ok':
			pop.dismiss()
		else:
			pass
	def open_tag_screen(self,tag_info):
		tag_screen = TagScreen()
		tag_screen.tag_name = tag_info
		for i in self.root_screen.current_screen.ids.screen_manager.screens:
			if i.name == 'tag_screen':
				self.root_screen.current_screen.ids.screen_manager.remove_widget(i)
		self.root_screen.current_screen.ids.screen_manager.transition = NoTransition()
		self.root_screen.current_screen.ids.screen_manager.add_widget(tag_screen)
		self.video_cache()
		self.root_screen.current_screen.ids.screen_manager.current = 'tag_screen'
	def change_screen(self,screen):
		self.video_cache()
		if self.root_screen.current != screen:
			self.root_screen.current = screen
		else:
			if screen == 'home_screen':
				screenobject = self.home_page
			elif screen == 'my_galaxy':
				screenobject = self.my_galaxy
			elif screen == 'challenges_screen':
				screenobject = self.challenge_screen
			#elif screen == 'notifications_screen':
			#	screenobject = self.notification_screen
			elif screen == 'my_profile':
				screenobject = self.my_profile
			if screenobject.ids.screen_manager.current != 'main':
				num_base = 1
				num_aim = len(screenobject.ids.screen_manager.screens)
				screenobject.ids.screen_manager.current = 'main'
				for i in range(num_base,num_aim):
					screenobject.ids.screen_manager.remove_widget(screenobject.ids.screen_manager.screens[1])
			else:
				anim = Animation(scroll_y = 1,t = 'linear')
				anim.start(screenobject.ids.main_scroll)
	def open_post(self,parameters):
		self.video_cache()
		info = parameters[0]
		print(info)
		media = parameters[1]
		image_screen = ImageScreen()
		for i in self.root_screen.current_screen.ids.screen_manager.screens:
			if i.name == 'image_screen':
				self.root_screen.current_screen.ids.screen_manager.remove_widget(i)
		self.root_screen.current_screen.ids.screen_manager.transition = NoTransition()
		self.root_screen.current_screen.ids.screen_manager.add_widget(image_screen)
		self.root_screen.current_screen.ids.screen_manager.current = 'image_screen'
		sub_info = self.check_sub_info(info)
		self.display_a_post(info,media,image_screen.ids.post_scroll,sub_info,image_screen.ids.post_scroll)

	def video_debug(self, video):
		global vid_video
		vid_video = video
		threading.Thread(target = self.video_video).start()
	def video_video(self):
		Clock.schedule_once(self.print_video, 1)
	def print_video(self,instance):
		global vid_video
		vid_video._video.eos = 'loop'
			
	def remove_tag(self,tag_root):
		self.posting_tags.remove(tag_root.text)
		tag_root.parent.remove_widget(tag_root)
		print(self.posting_tags)
	def open_gallery_images(self):
		self.video_cache()
		if self.post_screen.ids.posting_media_layout.active == False or self.post_screen.upload_mode == 'Image':
			if not self.gallery_images:
				self.gallery_images = GalleryImages()
				self.gallery_images.open()
				images = []
				for r,d,f in os.walk("assets/"):
					for file in f:
						print(file)
						if file.endswith(".jpg"):
							images.append(os.path.join(r,file))
						elif file.endswith(".JPG"):
							images.append(os.path.join(r,file))
						elif file.endswith(".jpeg"):
							images.append(os.path.join(r,file))
				for i in images:
					t = os.path.getmtime(i)
					mod_time = datetime.datetime.fromtimestamp(t)
					mod_hour = datetime.datetime(*mod_time.timetuple()[:3])
					image = GalleryFitImageTouch(source =i,size_hint = (1,None),press_callback = self.select_image_post)
					image.height = (self.window.width/3)-dp(8)
					image.press_parameter = image
					image.select_mode = self.gallery_images
					self.gallery_images.ids.gallery_scroll.add_widget(image)
			else:
				self.gallery_images.open()
			self.post_screen.upload_mode = 'Image'
		else:
			self.posting_warning_dialog(self.open_gallery_images)
	def posting_warning_dialog(self,base_callback):
		self.video_cache()
		global base
		base = base_callback
		posting_warning_dialog = WarningPopup(
			message="Your saved changes will be lost.",
			callback=self.posting_warning_dialog_callback)
		posting_warning_dialog.open()
	def posting_warning_dialog_callback(self,args):
		global base
		if args=='Ok':
			self.posting_register.clear()
			self.gallery_images = None
			self.gallery_audio = None
			self.gallery_video = None
			self.posting_video_lay = None
			self.posting_audio_lay = None
			self.post_screen.ids.posting_media_layout.clear_widgets()
			self.post_screen.ids.posting_media_layout.active = False
			base()
		else:
			pass
	def	gallery_images_dialog(self,popup):
		global pop
		pop = popup
		post_warning_dialog = WarningPopup(
			message="Your post changes will be lost.",
			callback=self.gallery_images_dialog_callback)
		post_warning_dialog.open()
	def gallery_images_dialog_callback(self,args):
		global pop 
		if args=='Ok':
			pop.dismiss()
			self.gallery_images = None
			self.posting_register.clear()
			self.display_selected_posts()
		else:
			pass
	def open_gallery_audio(self):
		self.video_cache()
		if self.post_screen.ids.posting_media_layout.active == False:
			if not self.gallery_audio:
				self.gallery_audio = GalleryAudio()
				self.gallery_audio.open()
				audio = []
				for r,d,f in os.walk("assets/"):
					for file in f:
						if file.endswith(".mp3"):
							audio.append(os.path.join(r,file))
						elif file.endswith(".wav"):
							audio.append(os.path.join(r,file))
				for i in audio:
					basename = os.path.basename(i)
					filename = os.path.splitext(basename)[0]
					size = (os.path.getsize(i)/(1024**2))
					rounded_size = round(size,1)
					sound = SoundLoader.load(i)
					duration = sound.length/60
					minn = (duration//1)
					decc = (duration%1)
					secc = (decc/100)*60
					duration = round((minn+secc),2)
					audio_layout = GalleryAudioLayout(source=i,name = filename, filesize = str(rounded_size),duration =str(duration))
					self.gallery_audio.ids.gallery_scroll.add_widget(audio_layout)
					self.gallery_audio.ids.gallery_scroll.add_widget(MDSeparator())

			else:
				self.gallery_audio.open()
			self.post_screen.upload_mode = 'Audio'
		else:
			self.posting_warning_dialog(self.open_gallery_audio)
	def select_audio_post(self,audio):
		self.gallery_audio.dismiss()
		post_audio_lay = PostScreenAudioLayout()
		if self.preview_audio:
			self.preview_audio.stop()
		self.preview_audio = None
		basename = os.path.basename(audio)
		name = os.path.splitext(basename)[0]
		self.posting_audio_lay = PostingAudioLayout(filename = str(name),audio = audio)
		post_audio_lay.clear_widgets()
		post_audio_lay.add_widget(self.posting_audio_lay)
		self.post_screen.ids.posting_media_layout.clear_widgets()
		self.post_screen.ids.posting_media_layout.add_widget(post_audio_lay)
		self.post_screen.ids.posting_media_layout.active = True
	def open_cover_image_select(self, layout):
		self.video_cache()
		self.gallery_images_single = GalleryImagesSingle()
		self.gallery_images_single.open()
		images = ["assets/blur trial.png"]
		for r,d,f in os.walk("assets/"):
			for file in f:
				if file.endswith(".jpg"):
					images.append(os.path.join(r,file))
				elif file.endswith(".JPG"):
					images.append(os.path.join(r,file))
		for i in images:
			image = FitImageTouch(source =i,size_hint = (1,None),press_callback = self.select_cover_image)
			image.height = (self.window.width/3)-dp(8)
			image.press_parameter = [image,layout,self.gallery_images_single]
			self.gallery_images_single.ids.gallery_scroll.add_widget(image)
	def select_cover_image(self, parameters):
		img = parameters[0]
		layout = parameters[1]
		popup = parameters[2]
		popup.dismiss()
		layout.clear_widgets()
		cv_image = AudioCoverImageSelect(source =img.source)
		self.posting_audio_lay.source = img.source
		layout.add_widget(cv_image)
	def open_gallery_video(self):
		self.video_cache()
		if self.post_screen.ids.posting_media_layout.active == False:
			if not self.gallery_video:
				self.gallery_video = GalleryVideo()
				self.gallery_video.open()
				images = []
				for r,d,f in os.walk("assets/"):
					for file in f:
						if file.endswith(".mp4"):
							images.append(os.path.join(r,file))
						elif file.endswith(".mkv"):
							images.append(os.path.join(r,file))
				for i in images:
					t = os.path.getmtime(i)
					mod_time = datetime.datetime.fromtimestamp(t)
					mod_hour = datetime.datetime(*mod_time.timetuple()[:3])
					thumbnail = create_video_thumbnail(i)
					print(thumbnail)
					image = FitVideoTouch(source =str(thumbnail),vid = i,size_hint = (1,None),press_callback = self.select_video_post)
					image.height = (self.window.width/3)-dp(8)
					image.press_parameter = image
					self.gallery_video.ids.gallery_scroll.add_widget(image)
			else:
				self.gallery_video.open()
			self.post_screen.upload_mode = 'Video'
		else:
			self.posting_warning_dialog(self.open_gallery_video)
	def select_video_post(self,video):
		self.video_cache()
		self.gallery_video.dismiss()
		post_video_lay = PostScreenVideoLayout()
		g = cv2.VideoCapture(video.vid)
		height = g.get(cv2.CAP_PROP_FRAME_HEIGHT)
		width = g.get(cv2.CAP_PROP_FRAME_WIDTH)
		hg = (self.window.width-dp(20))/(width/height)
		if hg > ((self.window.height)-dp(60)):
			n_hg = ((self.window.height)-dp(60))
			self.posting_video_lay = PostVideo(root_layout = self.post_screen.ids.posting_media_layout,source = video.vid, thumbnail = video.source,aspect_ratio = (width/height),size_hint = (1,None),height = n_hg)
			self.posting_video_lay.ids.blur.ratio = height/width
			self.posting_video_lay.ids.video_blur.effects = [PixelateEffect(pixel_size = 1.5),HorizontalBlurEffect(size = 15)]
		else:
			self.posting_video_lay = PostVideo(root_layout = self.post_screen.ids.posting_media_layout,source = video.vid, thumbnail = video.source,aspect_ratio = (width/height),size_hint = (1,None),height = hg)
		post_video_lay.clear_widgets()
		post_video_lay.add_widget(self.posting_video_lay)
		self.post_screen.ids.posting_media_layout.clear_widgets()
		self.post_screen.ids.posting_media_layout.add_widget(post_video_lay)
		self.post_screen.ids.posting_media_layout.active = True
	def select_image_post(self,img):
		if img.selected == False:
			if len(self.posting_register)<10:
				img.selected = True
				self.posting_register.append(img.source)
				self.gallery_images.ids.post_count.count = str(len(self.posting_register))
				self.gallery_images.ids.post_check.p_c = int(len(self.posting_register))
				print(len(self.posting_register))
			else:
				toast('There is a max of 10 photos per post!')
		else:
			img.selected =False
			self.posting_register.remove(img.source)
			self.gallery_images.ids.post_count.count = str(len(self.posting_register))
			self.gallery_images.ids.post_check.p_c = int(len(self.posting_register))
			print(len(self.posting_register))
	def display_selected_posts(self):
		print('Enter')
		self.post_screen.ids.posting_media_layout.clear_widgets()
		post_image_lay = PostScreenImageLayout()
		for i in self.posting_register:
			self.gallery_images.ids.post_count.count = str(len(self.posting_register))
			image = FitImageTouch(source = i,size_hint = (None,None),size = (((self.window.width-dp(30))/3),((self.window.width-dp(30))/3)))
			post_image_lay.add_widget(image)
		self.post_screen.ids.posting_media_layout.add_widget(post_image_lay)
		if len(self.posting_register)>0:
			self.post_screen.ids.posting_media_layout.active = True
	def upload_post(self, mode,caption,emotion):
		self.video_cache()
		if mode == 'Image':
			if self.posting_register == []:
				pass
			else:
				i = self.posting_register
				trial = Image(source = i[0])
				img_ratio = trial.image_ratio
				post_idd = str('User/'+str(self.user)+'-'+str(self.user_post_count+1))
				current_post_count = self.user_post_count+1
				print(post_idd)
				log_popup = LoginProcess()
				log_popup.ids.log_message.text = "Uploading...."
				log_popup.open()
				upload_post_sql = "INSERT INTO `posts`(`Userid`,`image_ratio`,`caption`,`type`,`post_id`,`emotion`) VALUES (%s,%s,%s,%s,%s,%s)"
				values =[self.user, img_ratio,caption,mode,post_idd,emotion]
				update_post_count_sql = "UPDATE `users` SET `post_count` =%s WHERE `Userid`=%s"
				upload_image_sql = "INSERT INTO `post_images`(`post_id`,`image`,`image_name`) VALUES (%s,%s,%s)"
				insert_tags_sql = "INSERT INTO `tags`(`post_id`,`tag_name`) VALUES (%s,%s)"
				try:
					self.dbconnection()
					self.mycursor.execute(upload_post_sql, values)
					num=0
					for f in i:
						num+=1
						image_name = (post_idd+'/'+mode+str(num))
						print(image_name)
						image_values = [post_idd, f, image_name]
						self.mycursor.execute(upload_image_sql,image_values)
					for i in self.posting_tags:
						self.mycursor.execute(insert_tags_sql,[post_idd,i])
					post_count_values = [current_post_count,self.user]
					self.mycursor.execute(update_post_count_sql,post_count_values)
					self.mydb.commit()
				except Exception as e:
					raise e
					log_popup.ids.log_message.text = "Check your Internet Connection"
					log_popup.ids.log_process_layout.remove_widget(log_popup.ids.log_spinner)
					log_popup.auto_dismiss = True
				else:
					print('Uploaded')
					log_popup.dismiss()
					self.user_post_count+=1
					self.root_manager.transition.direction = 'left'
					self.root_manager.current = 'basic_root'
					self.posting_register = []
					self.posting_tags.clear()
					self.root_manager.remove_widget(self.post_screen)
					self.post_screen = PostScreen()
					self.post_screen.ids.profile_pic.source = self.profile_pic
					self.root_manager.add_widget(self.post_screen)
					self.gallery_images = None
		elif mode == 'Audio':
			if self.posting_audio_lay:
				cover_image = self.posting_audio_lay.source
				title = self.posting_audio_lay.ids.title.text
				audio = self.posting_audio_lay.audio
				post_idd = str('User/'+str(self.user)+'-'+str(self.user_post_count+1))
				current_post_count = self.user_post_count+1
				log_popup = LoginProcess()
				log_popup.ids.log_message.text = "Uploading...."
				log_popup.open()
				upload_post_sql = "INSERT INTO `posts`(`Userid`,`caption`,`type`,`post_id`,`emotion`) VALUES (%s,%s,%s,%s,%s)"
				values =[self.user,caption,mode,post_idd,emotion]
				update_post_count_sql = "UPDATE `users` SET `post_count` =%s WHERE `Userid`=%s"
				upload_audio_sql = "INSERT INTO `post_audio`(`post_id`,`audio`,`audio_name`,`title`,`cover_photo`) VALUES (%s,%s,%s,%s,%s)"
				insert_tags_sql = "INSERT INTO `tags`(`post_id`,`tag_name`) VALUES (%s,%s)"
				try:
					self.dbconnection()
					self.mycursor.execute(upload_post_sql, values)
					audio_name = (post_idd+'/'+mode)
					audio_values = [post_idd, audio, audio_name,title,cover_image]
					self.mycursor.execute(upload_audio_sql,audio_values)
					for i in self.posting_tags:
						self.mycursor.execute(insert_tags_sql,[post_idd,i])
					post_count_values = [current_post_count,self.user]
					self.mycursor.execute(update_post_count_sql,post_count_values)
					self.mydb.commit()
				except Exception as e:
					raise e
					log_popup.ids.log_message.text = "Check your Internet Connection"
					log_popup.ids.log_process_layout.remove_widget(log_popup.ids.log_spinner)
					log_popup.auto_dismiss = True
				else:
					print('Uploaded')
					log_popup.dismiss()
					self.user_post_count+=1
					self.root_manager.transition.direction = 'left'
					self.root_manager.current = 'basic_root'
					self.posting_register = []
					self.posting_tags.clear()
					self.root_manager.remove_widget(self.post_screen)
					self.post_screen = PostScreen()
					self.post_screen.ids.profile_pic.source = self.profile_pic
					self.root_manager.add_widget(self.post_screen)
					self.gallery_images = None
		elif mode == 'Video':
			if self.posting_video_lay:
				vid = self.posting_video_lay.source
				thumbnail = self.posting_video_lay.thumbnail
				ratio = self.posting_video_lay.aspect_ratio
				post_idd = str('User/'+str(self.user)+'-'+str(self.user_post_count+1))
				current_post_count = self.user_post_count+1
				log_popup = LoginProcess()
				log_popup.ids.log_message.text = "Uploading...."
				log_popup.open()
				upload_post_sql = "INSERT INTO `posts`(`Userid`,`caption`,`type`,`post_id`,`image_ratio`,`emotion`) VALUES (%s,%s,%s,%s,%s,%s)"
				values =[self.user,caption,mode,post_idd,ratio,emotion]
				update_post_count_sql = "UPDATE `users` SET `post_count` =%s WHERE `Userid`=%s"
				upload_video_sql = "INSERT INTO `post_video`(`post_id`,`video`,`video_name`,`thumbnail`) VALUES (%s,%s,%s,%s)"
				insert_tags_sql = "INSERT INTO `tags`(`post_id`,`tag_name`) VALUES (%s,%s)"
				try:
					self.dbconnection()
					self.mycursor.execute(upload_post_sql, values)
					video_name = (post_idd+'/'+mode)
					video_values = [post_idd, vid, video_name,thumbnail]
					self.mycursor.execute(upload_video_sql,video_values)
					for i in self.posting_tags:
						self.mycursor.execute(insert_tags_sql,[post_idd,i])
					post_count_values = [current_post_count,self.user]
					self.mycursor.execute(update_post_count_sql,post_count_values)
					self.mydb.commit()
				except Exception as e:
					raise e
					log_popup.ids.log_message.text = "Check your Internet Connection"
					log_popup.ids.log_process_layout.remove_widget(log_popup.ids.log_spinner)
					log_popup.auto_dismiss = True
				else:
					print('Uploaded')
					log_popup.dismiss()
					self.user_post_count+=1
					self.root_manager.transition.direction = 'left'
					self.root_manager.current = 'basic_root'
					self.posting_register = []
					self.posting_tags.clear()
					self.root_manager.remove_widget(self.post_screen)
					self.post_screen = PostScreen()
					self.post_screen.ids.profile_pic.source = self.profile_pic
					self.root_manager.add_widget(self.post_screen)
					self.gallery_images = None

	def bottomnav_custom(self,screen):
		pass 
	def video_cache(self):
		if self.playing_video:
			self.playing_video.state = 'pause'
	def close_screen(self, screen):
		self.video_cache()
		manager = self.root_screen.current_screen.ids.screen_manager
		manager.remove_widget(screen)
		screens = self.root_screen.current_screen.ids.screen_manager.screens
		num = len(self.root_screen.current_screen.ids.screen_manager.screens)
		manager.current = (screens[num-1]).name

	def log_out(self):
		self.video_cache()
		global logo_layout
		logo_layout.clear_widgets()
		self.root.clear_widgets()
		self.log = False
		self.user = None
		self.user_info = []
		self.interests = []
		self.home_index = 0
		self.home_buffer = False
		self.post_thread_list = []
		self.displaying_posts_list = []
		self.scroll_pos_y = 0
		self.refreshed = False
		self.comments_screen = None
		self.home_screenimg = []
		self.challenge_screenimg = []
		self.my_galaxyimg = []
		self.notifications_screenimg = []
		self.gallery_images = None
		self.gallery_audio = None
		self.gallery_video = None
		if self.playing_sound:
			self.playing_sound.stop()
		self.playing_sound = None
		self.playing_sound_source = None
		self.played_sounds = []
		self.played_preview_audio = []
		self.stopped_playing_sound = None
		self.preview_audio = None
		self.preview_audio_source = None
		self.playing_video = None
		self.posting_register = []
		self.posting_tags = []
		self.live_pinned_users = []
		self.live_unpinned_users = []
		self.live_blocked_users = []
		self.live_unblocked_users = []
		self.posting_audio_lay = None
		self.posting_video_lay = None
		self.build()
class DynamicLabel(MDLabel):
	virtual_height = NumericProperty()
	short_height = NumericProperty()
class MyCard(MDCard):
	pass
class LoginProcess(ModalView):
	pass
class LoginProcessNotification(BoxLayout):
	pass
class _RefreshScrollEffect(DampedScrollEffect):
    """This class is simply based on DampedScrollEffect.
    If you need any documentation please look at kivy.effects.dampedscrolleffect.
    """

    min_scroll_to_reload = NumericProperty("-100dp")
    """Minimum overscroll value to reload."""

    def on_overscroll(self, scrollview, overscroll):
        if overscroll < self.min_scroll_to_reload:
            scroll_view = self.target_widget.parent
            scroll_view._did_overscroll = True
            return True
        else:
            return False
class MyRecycleView(RecycleView):
	def __init__(self, **kargs):
		super().__init__(**kargs)
		self._work_spinnrer = False
		self._did_overscroll = False
		self.refresh_spinner = None
	def on_end_event(self):
		pass
	'''def on_scroll_stop(self, *args,**kwargs):
		result = super(MyRecycleView, self).on_scroll_stop(*args, **kwargs)
		#and scroll_distance = 50
		if self.scroll_y == 1 and hasattr(self, 'on_end_event'):
			if self.refresh_callback:
				self.refresh_callback()
				print (self.refresh_callback)
			if not self.refresh_spinner:
				self.refresh_spinner = RefreshSpinner(_refresh_layout=self)
				print(self.root_layout)
				self.root_layout.add_widget(self.refresh_spinner)
			self.refresh_spinner.start_anim_spinner()
			self._did_overscroll = False
			return True
		return super().on_touch_up(*args)'''
	
class RefreshSpinner(ThemableBehavior, FloatLayout):
    spinner_color = ListProperty([1, 1, 1, 1])

    _refresh_layout = ObjectProperty()
    """kivymd.refreshlayout.MDScrollViewRefreshLayout object."""

    def start_anim_spinner(self):
        spinner = self.ids.body_spinner
        Animation(
            y=spinner.y - self.theme_cls.standard_increment * 2 + dp(10),
            d=0.8,
            t="out_elastic",
        ).start(spinner)

    def hide_anim_spinner(self):
        spinner = self.ids.body_spinner
        anim = Animation(y=Window.height, d=0.8, t="out_elastic")
        anim.bind(on_complete=self.set_spinner)
        anim.start(spinner)

    def set_spinner(self, *args):
        body_spinner = self.ids.body_spinner
        body_spinner.size = (dp(46), dp(46))
        body_spinner.y = Window.height
        body_spinner.opacity = 1
        spinner = self.ids.spinner
        spinner.size = (dp(30), dp(30))
        spinner.opacity = 1
        self._refresh_layout._work_spinnrer = False
        self._refresh_layout._did_overscroll = False
    
class ImageScreen(Screen):
	source = ""
class PinsScreen(Screen):
	info = ListProperty([])
	title = StringProperty('')
	profile_pic = StringProperty('')
class LikeScreen(Screen):
	info = ListProperty([])
class CommentScreen(ModalView):
	info = ListProperty([])
	likecomment = ObjectProperty()
class MyProfileScreen(Screen):
	active= False
	connected = True
	reposts_active = False
	saved_active = False
	pins_count = NumericProperty(-1)
	pinned_count = NumericProperty(-1)
	def on_enter(self):
		if self.connected:
			self.user_info = running_app.user_info
		else:
			self.user_info = running_app.backup_user_info
		Clock.schedule_once(self.display_info, 0)
	def display_info(self,instance):
		if not self.active:
			try:
				if self.ids.fullname.text =='':
					self.ids.fullname.height = 0
				if self.ids.portofolio.text =='':
					self.ids.portofolio.height = 0
				if self.ids.bio.text =='':
					self.ids.bio.height = 0
				self.ids.username.text= self.user_info[2]
				self.ids.profilepic.source= running_app.profile_pic
				self.ids.fullname.text= self.user_info[1]
				if self.ids.fullname.text == '':
					self.ids.fullname.height = 0
				else:
					self.ids.fullname.height = dp(15)
				self.ids.bio.text= self.user_info[9]
				self.ids.portofolio.text= self.user_info[10]
				if self.ids.portofolio.text == '':
					self.ids.portofolio.height = 0
				else:
					self.ids.portofolio.height = dp(15)
				self.ids.scrn_manager.transition = NoTransition()
				before = self.ids.bio._label.render()
				self.ids.bio.text_size=((Pulsar().window.width - dp(40)), None)
				after = self.ids.bio._label.render()
				if self.ids.bio.text == '':
					self.ids.bio.height = dp(0)
				else:
					self.ids.bio.height = (after[1]/before[1])*before[1]
				self.ids.info_layout.height=(dp(40)+self.ids.bio.height+self.ids.portofolio.height)
				count_pins_sql = "SELECT COUNT(*) FROM `pins` WHERE `pinned_id`= %s OR `pinned_id`= %s"
				count_pinned_sql = "SELECT COUNT(*) FROM `pins` WHERE `Userid`= %s OR `Userid`= %s"
				running_app.mycursor.execute(count_pins_sql, [running_app.user,running_app.user])
				pins_result = running_app.mycursor.fetchone()
				pins_count = ''.join(map(str, pins_result))
				self.pins_count = int(pins_count)
				running_app.mycursor.execute(count_pinned_sql, [running_app.user,running_app.user])
				pinned_result = running_app.mycursor.fetchone()
				pinned_count = ''.join(map(str, pinned_result))
				self.pinned_count = int(pinned_count)
				running_app.display_user_posts(running_app.user,self.ids.grid_layout,self)
			except Exception as e:
				print(e)
				toast('Check Your Internet Connection')
				self.connected = False
				self.on_enter()
			else:
				if self.connected:
					self.active = True
				self.connected = True
	def display_reposts(self):
		Clock.schedule_once(partial(self.display_reposts_buffer),0)
	def display_reposts_buffer(self,instance):
		running_app.display_user_reposts(running_app.user,self.ids.repost_layout,self.ids.my_profile_layout,self.ids.repost_screen)
		self.reposts_active = True
	def display_saved(self):
		Clock.schedule_once(partial(self.display_saved_buffer),0)
	def display_saved_buffer(self,instance):
		running_app.display_user_saved_posts(running_app.user,self.ids.saved_layout,self.ids.my_profile_layout,self.ids.saved_screen)
		self.saved_active = True
	def refresh_function(self):
		running_app.video_cache()
		user_sql = "SELECT * FROM `users` WHERE UserId = %s OR DOR = %s"
		try:
			running_app.dbconnection()
			running_app.mycursor.execute(user_sql,[running_app.user,running_app.user])
			result = running_app.mycursor.fetchone()
			running_app.user_info = result
			running_app.user_post_count = result[11]
		except Exception as e:
			toast('Check your Internet Connection')
		else:
			Clock.schedule_once(self.refresh_buffer, 3)
	def refresh_buffer(self,instance):
		self.active=False
		self.on_enter()
		running_app.refresh_done()
class EditProfileScreen(ModalView):
	pass
class ProfileScreen(Screen):
	username = StringProperty('')
	profile_pic = StringProperty('')
	fullname = StringProperty('')
	bio = StringProperty('')
	portofolio = StringProperty('')
	info = ListProperty([])
	user = None
	pinned = BooleanProperty(False)
	pins_count = NumericProperty(-1)
	pinned_count = NumericProperty(-1)
	post_count= NumericProperty(-1)
	active= False
	reposts_active = False
	def on_enter(self):
		if not self.active:
			user_sql = "SELECT `FullName`,`ProfilePicture`,`Bio`,`Portofolio`  FROM `users` WHERE UserId = %s OR DOR = %s"
			try:
				running_app.dbconnection()
				running_app.mycursor.execute(user_sql,[self.info[0],self.info[0]])
				result = running_app.mycursor.fetchone()
				self.user_info = result
				count_pinned_sql = "SELECT COUNT(*) FROM `pins` WHERE `Userid`= %s OR `Userid`= %s"
				count_pins_sql = "SELECT COUNT(*) FROM `pins` WHERE `pinned_id`= %s OR `pinned_id`= %s"
				count_posts_sql = "SELECT COUNT(*) FROM `posts` WHERE `Userid`= %s OR `Userid`= %s"
				running_app.mycursor.execute(count_pins_sql, [self.info[0],self.info[0]])
				pins_result = running_app.mycursor.fetchone()
				pins_db_count = ''.join(map(str, pins_result))
				self.pins_count = int(pins_db_count)
				running_app.mycursor.execute(count_pinned_sql, [self.info[0],self.info[0]])
				pinned_result = running_app.mycursor.fetchone()
				pinned_db_count = ''.join(map(str, pinned_result))
				self.pinned_count = int(pinned_db_count)
				running_app.mycursor.execute(count_posts_sql, [self.info[0],self.info[0]])
				posts_result = running_app.mycursor.fetchone()
				posts_db_count = ''.join(map(str, posts_result))
				self.post_count = int(posts_db_count)
				running_app.display_user_posts(self.info[0],self.ids.grid_layout,self)
				self.ids.grid_layout.height = self.ids.grid_layout.minimum_height
				self.ids.grid_layout.pos_hint = {'top':1}
			except Exception as e:
				print(e)
				toast('Check Your Internet Connection')
			else:
				self.ids.fullname.text = self.user_info[0]
				self.profile_pic = self.user_info[1]
				self.ids.bio.text = self.user_info[2]
				self.ids.portofolio.text = self.user_info[3]
				if self.ids.bio.text == '':
					self.ids.bio.height = 0
				else:
					before = self.ids.bio._label.render()
					self.ids.bio.text_size=((Pulsar().window.width - dp(40)), None)
					after = self.ids.bio._label.render()
					self.ids.bio.height = (after[1]/before[1])*before[1]
				if self.ids.fullname.text == '':
					self.ids.fullname.height = 0
				else:
					self.ids.fullname.height = dp(15)
				if self.ids.portofolio.text == '':
					self.ids.portofolio.height = 0
				else:
					self.ids.portofolio.height = dp(15)
				self.ids.info_layout.height=(dp(40)+self.ids.bio.height+self.ids.portofolio.height)
				self.active = True
	def display_reposts(self):
		Clock.schedule_once(partial(self.display_reposts_buffer),0)
	def display_reposts_buffer(self,instance):
		running_app.display_user_reposts(self.info[0],self.ids.repost_layout,self.ids.profile_scroll_layout,self.ids.repost_screen)
		self.reposts_active = True
	
class TagScreen(Screen):
	tag_name = StringProperty('')
	post_count = NumericProperty(-1)
	tag_cover_pic = StringProperty('assets/purple.jpg')
	tag_profile_pic = StringProperty('assets/purple.jpg')
	def on_enter(self):
		count_posts_sql = "SELECT COUNT(*) FROM `tags` WHERE `tag_name`= %s"
		print(count_posts_sql)
		running_app.dbconnection()
		running_app.mycursor.execute(count_posts_sql,[self.tag_name,])
		post_result = running_app.mycursor.fetchone()
		post_db_count = ''.join(map(str, post_result))
		self.post_count = int(post_db_count)
		galaxy_tags_posts_sql = "SELECT tags.tag_name,post_images.image FROM `tags` INNER JOIN `posts` INNER JOIN `post_images` ON posts.post_id = tags.post_id AND posts.post_id = post_images.post_id WHERE tags.tag_name = %s AND posts.type = 'Image' ORDER BY posts.id DESC LIMIT 3"
		running_app.mycursor.execute(galaxy_tags_posts_sql,(self.tag_name,))
		tag_posts = running_app.mycursor.fetchall()
		print(tag_posts)
		if len(tag_posts)>0:
			self.tag_cover_pic = (tag_posts[0][1])
		if len(tag_posts)>1:
			self.tag_profile_pic = (tag_posts[0][0])
		running_app.display_tag_posts(self.tag_name,self.ids.recent_layout,self)
	def trending_enter(self):
		running_app.display_tag_posts(self.tag_name,self.ids.trending_layout,self)
class MessageScreen(Screen):
	pass
class MessagingScreen(Screen):
	pass
class MyRecycleBoxLayout(RecycleBoxLayout):
	pass
class RefreshScrollView(MyRecycleView,MDScrollViewRefreshLayout):
	pass
class AudioLayout(BoxLayout):
	source = StringProperty(None)
	info = NumericProperty(dp(80))
	caption = StringProperty(None)
	cover = StringProperty('assets/guitar-1139397_1280_tile_crop.png')
	profilepic = StringProperty('None')
	username = StringProperty('None')
	title = StringProperty('Title')
	post_info = ListProperty()
	likes = NumericProperty(0)
	comments = NumericProperty(0)
	like_comment_info = ListProperty()
	scroll_layout = ObjectProperty()
	pinned = BooleanProperty(False)
	blocked = BooleanProperty(False)
	emotion = StringProperty('')
class ImageLayout(BoxLayout):
	source = StringProperty(None)
	post_height = NumericProperty(dp(365)) 
	info = NumericProperty(dp(80))
	caption = StringProperty(None)
	virtual_height = NumericProperty(None)
	profilepic = StringProperty('None')
	username = StringProperty('None')
	post_info = ListProperty()
	scroll_layout = ObjectProperty()
	likecomment = ObjectProperty(None)
	pinned = BooleanProperty(False)
	emotion = StringProperty('')
	blocked = BooleanProperty(False)
class ImageLayoutMultiple(BoxLayout):
	source = StringProperty(None)
	post_height = NumericProperty(dp(365)) 
	info = NumericProperty(dp(80))
	caption = StringProperty(None)
	virtual_height = NumericProperty(None)
	profilepic = StringProperty('None')
	username = StringProperty('None')
	post_info = ListProperty()
	pinned = BooleanProperty(False)
	likecomment = ObjectProperty(None)
	scroll_layout = ObjectProperty()
	emotion = StringProperty('')
	blocked = BooleanProperty(False)
class MultipleImageIndex(BoxLayout):
	carousel = ObjectProperty()
	num = NumericProperty()
class VideoLayout(BoxLayout):
	source = StringProperty(None)
	thumbnail = StringProperty(None)
	post_height = NumericProperty(dp(365)) 
	info = NumericProperty(dp(80))
	caption = StringProperty(None)
	virtual_height = NumericProperty(None)
	profilepic = StringProperty('None')
	username = StringProperty('None')
	post_info = ListProperty()
	scroll_layout = ObjectProperty()
	likecomment = ObjectProperty(None)
	pinned = BooleanProperty(False)
	emotion = StringProperty('')
	blocked = BooleanProperty(False)
class PostVideo(BoxLayout):
	source = StringProperty(None)
	thumbnail = StringProperty(None)
	aspect_ratio = NumericProperty(None)
	root_layout = ObjectProperty(None)
class VideoDisplayUnit(RectangularElevationBehavior,BoxLayout):
	source = StringProperty(None)
	thumbnail = StringProperty(None)
	profile_pic = StringProperty(None)
	num = NumericProperty()
	base = ObjectProperty()
	state = StringProperty('pause')
	scrn = StringProperty('')
	mng = ObjectProperty()
	info = ListProperty([])
	sub_info = ListProperty([])
	pinned = BooleanProperty(False)
class DisplayingVideo(BoxLayout):
	source = StringProperty(None)
	thumbnail = StringProperty(None)
	aspect_ratio = NumericProperty(None)
	state = StringProperty('pause')
	index = NumericProperty(0)
	root_layout = ObjectProperty(None)
class ImageTouch(ButtonBehavior, Image):
	user = NumericProperty(1)
class ImageBGEXT(BoxLayout):
	source = StringProperty(None)
class RoundImageTouch(CircularRippleBehavior,ButtonBehavior, BoxLayout):
	source = StringProperty(None)
class RoundImage(BoxLayout):
	source = StringProperty(None)
class ScreenChangerLayout(CircularRippleBehavior, ButtonBehavior, BoxLayout):
	source = StringProperty("")
class FullScreen(BoxLayout):
	pass
class PostInfo(BoxLayout):
	pass
class LoginScreen(BoxLayout):
	pass
class InterestScreen(BoxLayout):
	pass
class InterestCard(BoxLayout):
	source = StringProperty('assets/purple.jpg')
	pres = StringProperty(None)
	sub = ListProperty(None)
	idd = StringProperty()
class InterestLayout(CircularRippleBehavior, ButtonBehavior, BoxLayout):
	pass
class CategoryCard(CircularRippleBehavior, ButtonBehavior, BoxLayout):
	source = StringProperty('assets/purple.jpg')
	text = StringProperty('Categories')
class InterestSubcategory(CircularRippleBehavior, ButtonBehavior, BoxLayout):
	source = StringProperty('assets/purple.jpg')
	pres = StringProperty(None)
	idd = StringProperty()
class IconButton_ToolTip(MDIconButton,MDTooltip):
	pass
class RootScreen(ScreenManager):
	pass

class HomePage(Screen):
	active = False
	def on_enter(self):
		#self.scroll_layout -add widget(myspinner)
		#followed by thread which will search for data
		#add posts to the layout
		if self.active == False:
			action = threading.Thread(target = self.posts_buffer)
			action.start()
			self.active = True
	def posts_buffer(self):
		Clock.schedule_once(self.load_posts, 0)
	def load_posts(self,instance):
		running_app.display_posts(running_app.user)
class ChallengeScreen(Screen):
	active = False
	def on_enter(self):
		if self.active == False:
			self.action = threading.Thread(target = self.buffer_image)
			self.action.start()
			self.active=True
	def buffer_image(self):
		Clock.schedule_once(self.change_image, 5)
	def change_image(self,instance):
		self.ids.image_carousel.anim_move_duration = 1.5
		self.ids.image_carousel.index+=1
		self.buffer_image()
class ChallengeDefinition(Screen):
	pass
class MyGalaxy(Screen):
	active = False
	video_active = BooleanProperty(False)
	def on_enter(self):
		if self.active == False:
			self.ids.personalised_tag.state = 'down'
			Clock.schedule_once(self.video_display, 0)#try subprocess
			self.active = True
	def on_leave(self):
		self.video_active = False
	def video_display(self,instance):
		running_app.display_galaxy_posts()

class NotificationScreen(Screen):
	pass
class PostScreen(Screen):
	upload_mode = StringProperty('Text')
class EditPostScreen(Screen):
	info = ListProperty([])
class CameraScreen(Screen):
	pass
class MenuScreen(Screen):
	pass
class RootManager(ScreenManager):
	pass
class MySpinner(MDSpinner):
	pass
class Rate(BoxLayout):
	post_info = ListProperty()
class LikeComment(BoxLayout):
	likes = NumericProperty(0)
	comments = NumericProperty(0)
	post_info = ListProperty(None)
class CommentLay(BoxLayout):
	post_info = ListProperty(None)
	likecomment = ObjectProperty(None)
class Time(BoxLayout):
	time = StringProperty('')
class LikesCard(BoxLayout):
	user_info = ListProperty(None)
	pinned = BooleanProperty(False)
class CommentsCard(BoxLayout):
	user_info = ListProperty(None)
	pinned = BooleanProperty(False)
	time = StringProperty('-')
class MessagesCard(ButtonBehavior, BoxLayout):
	pass
class MessageLabel(BoxLayout):
	color = ListProperty([1,1,1,1])
class ElevatedIconButton(CircularElevationBehavior,MDIconButton):
	pass
class HeartIcon(MDIconButton):
	pass
class ImgHeartIcon(MDIconButton):
	pass
class CloseIcon(MDIconButton):
	pass
class PinIcon(MDIconButton):
	pass
class TypeInput(BoxLayout):
	hint = StringProperty()
class TagCard(Label):
	tag_info = StringProperty()
class ChallengeCard(RectangularElevationBehavior,ButtonBehavior,BoxLayout):
	source = StringProperty('')
	profile_pic =StringProperty('')
class ChallengeLayout(BoxLayout):
	pass
class ChallengePostLayout(BoxLayout):
	pass
class ChallengePostCard(ButtonBehavior,MDCard):
	pass
class PeopleCard(RectangularElevationBehavior,ButtonBehavior,BoxLayout):
	cover_image = StringProperty('assets/purple.jpg')
	profile_pic = StringProperty('assets/challenges.jpg')
	username = StringProperty('Username')
	info = ListProperty([])
	pinned = BooleanProperty(False)
class MyGalaxyGallery(BoxLayout):
	title = StringProperty()
	collection = ListProperty([])
	call = StringProperty()
class MyGalaxyVideos(BoxLayout):
	pass
class SearchCard(RectangularRippleBehavior,ButtonBehavior,BoxLayout):
	info = ListProperty([])
class PeopleLayout(BoxLayout):
	title = StringProperty()
class PinCard(BoxLayout):
	pass
class LikedCard(BoxLayout):
	pass
class CommentedCard(BoxLayout):
	pass
class RepostedCard(BoxLayout):
	pass
class TabsBase(BoxLayout,MDTabsBase):
	pass
class MeTabs(MDTabs,BoxLayout):
	pass
class SearchScreen(Screen):
	pass
class ButtonBoxLayout(RectangularRippleBehavior,ButtonBehavior,BoxLayout):
	pass
class GalleryImages(ModalView):
	pass
class GalleryImagesSingle(ModalView):
	pass
class PostingAudioLayout(MDCard):
	filename = StringProperty(None)
	audio = StringProperty(None)
	source = StringProperty('assets/my_pic.jpg')
class PostScreenImageLayout(GridLayout):
	active = BooleanProperty(False)
class PostScreenAudioLayout(BoxLayout):
	active = BooleanProperty(False)
class PostScreenVideoLayout(BoxLayout):
	active = BooleanProperty(False)
class PostScreenPostingLayout(BoxLayout):
	active = BooleanProperty(False)
	mode = StringProperty('')
class GalleryAudio(ModalView):
	pass
class GalleryAudioLayout(ButtonBehavior,BoxLayout):
	name = StringProperty(None)
	duration = StringProperty('Duration')
	filesize = StringProperty('Size')
	source = StringProperty(None)
class AudioCoverImageSelect(RelativeLayout):
	source = StringProperty('assets/my_pic.jpg')
class GalleryVideo(ModalView):
	pass

class FitImageTouch(ButtonBehavior,FitImage):
	press_callback = ObjectProperty(None)
	press_parameter = ObjectProperty()
	select_mode = ObjectProperty()
	selected = BooleanProperty(False)
	def on_press(self):
		if self.press_callback:
			self.press_callback(self.press_parameter)
class GalleryFitImageTouch(ButtonBehavior, BoxLayout):
	press_callback = ObjectProperty(None)
	press_parameter = ObjectProperty()
	source = StringProperty(None)
	select_mode = ObjectProperty()
	selected = BooleanProperty(False)
	def on_press(self):
		if self.press_callback:
			self.press_callback(self.press_parameter)
class FitMultipleImageTouch(ButtonBehavior, BoxLayout):
	press_callback = ObjectProperty(None)
	press_parameter = ObjectProperty()
	source = StringProperty(None)
	select_mode = ObjectProperty()
	selected = BooleanProperty(False)
	def on_press(self):
		if self.press_callback:
			self.press_callback(self.press_parameter)
class FitAudioTouch(ButtonBehavior, BoxLayout):
	press_callback = ObjectProperty(None)
	press_parameter = ObjectProperty()
	source = StringProperty(None)
	select_mode = ObjectProperty()
	selected = BooleanProperty(False)
	def on_press(self):
		if self.press_callback:
			self.press_callback(self.press_parameter)
class FitVideoTouch(ButtonBehavior, BoxLayout):
	press_callback = ObjectProperty(None)
	press_parameter = ObjectProperty()
	source = StringProperty(None)
	select_mode = ObjectProperty()
	selected = BooleanProperty(False)
	vid = StringProperty()
	def on_press(self):
		if self.press_callback:
			self.press_callback(self.press_parameter)
class BlurVideoBg(EffectWidget):
	ratio = NumericProperty(1)
	effects = [PixelateEffect(pixel_size = 1.5),HorizontalBlurEffect(size = 15)]
class NotificationCount(CircularElevationBehavior,BoxLayout):
	count = StringProperty()
class IconButton(ButtonBehavior, MDIcon):
	pass

class MyOuterScrollView(ScrollView):
	inner_scroll = ObjectProperty()
	inner_scroll_layout = ObjectProperty()
	parameter1 = ListProperty()
	def on_touch_down(self,touch):
		x,y = self.to_widget(*self.to_window(*touch.pos))
		if self.inner_scroll_layout.collide_point(x,y):
			touch.pos = (x,y)
			for i in self.parameter1:
				if i[0].current == i[1]:
					return i[2].on_touch_down(touch)
		else:
			return super(MyOuterScrollView, self).on_touch_down(touch)
class MyInnerScrollView(ScrollView):
	scroll_pos_y = NumericProperty(0)
	outer_scroll = ObjectProperty()
	static_scroll_y = NumericProperty(1)
	def on_touch_down(self,touch):
		self.static_scroll_y = self.scroll_y
		return super(MyInnerScrollView, self).on_touch_down(touch)
class MyGalaxyTags(MDRoundFlatButton, MDToggleButton):
    def __init__(self, **kwargs):
    	self.allow_no_selection = False
    	self.background_normal = [0,0,0,0]
    	self.background_down = [.85,.1,1,.85]
    	self.text_color_down = [1,1,1,1]
    	self.text_color_normal = [0,0,0,1]
    	super().__init__(**kwargs)
class MyGalaxyPostDisplay(BoxLayout):
	pass
class MyGalaxyPostDisplayUnit(RectangularElevationBehavior,ButtonBehavior,BoxLayout):
	info = ListProperty([])
	sub_info = ListProperty([])
	pinned = BooleanProperty(False)
class MyGalaxyAudioDisplay(BoxLayout):
	audio = ListProperty([])
	source = ListProperty([])
	sub_info = ListProperty([])
	pinned = ListProperty([])
	index = NumericProperty(0)
class MyGalaxyAudioProfile(RoundImageTouch):
	pinned = BooleanProperty(False)
class ElavatedBoxLayout(RectangularElevationBehavior,BoxLayout):
	pass
class WarningPopup(ModalView):
	message = StringProperty()
	callback = ObjectProperty()
class ConfirmationPopup(ModalView):
	message = StringProperty()
	callback = ObjectProperty()
	parameters = ListProperty([])
class PostOptions(ModalView):
	post_info = ListProperty()
	root_post = ObjectProperty()
class SelfPostOptions(ModalView):
	post_info = ListProperty()
	root_post = ObjectProperty()
class MyStackLayout(BoxLayout):
	pass
class ButtonBoxLayoutPlain(ButtonBehavior,BoxLayout):
	pass
class MyTextButton(ButtonBehavior,MDLabel):
	pass
class PostTagsLayout(BoxLayout):
	short_height = NumericProperty()
	real_height = NumericProperty()
	parent_layout = ObjectProperty()
	root_layout = ObjectProperty()
	label = ObjectProperty(Label())
	scroll_layout = ObjectProperty()
class DiscoverTagsLayout(BoxLayout):
	pass
class DiscoverTagsCard(RectangularElevationBehavior,ButtonBehavior,BoxLayout):
	info = StringProperty('')
	pics = ListProperty([])
class LinkTextButton(TouchBehavior,MDTextButton):
	long_touch = False
	def on_release(self):
		if not self.long_touch:
			print('Pressed')
		self.long_touch = False
	def on_long_touch(self, *args):
		self.long_touch = True
		Clipboard.copy(self.text)
		toast('Link Copied')
class TagsTextInput(MDTextField):
	layout = ObjectProperty()
	def on_text(instance,self, value):
		if (len(self.text))<25:
			for i in self.text:
				if i not in acceptaple_char and (i.lower()) not in acceptaple_char:
					old_text = self.text
					new_text = old_text.replace(i, '')
					self.text= new_text
					toast(str(i+' is not allowed'))
			if ' ' in self.text:
				if len(running_app.posting_tags)<=30:
					typed_text = self.text
					tag_text = typed_text.replace(' ', '')
					if ('#'+tag_text) in running_app.posting_tags:
						old_text = self.text
						new_text = old_text[:-1]
						self.text = new_text
						toast('You have already tagged this hastag')
					else:
						self.text = ''
						if tag_text!='':
							new_tag_text =('#'+tag_text)
							self.layout.add_widget(ChosenTagsCard(text = new_tag_text))
							running_app.posting_tags.append(new_tag_text)
				else:
					old_text = self.text
					new_text = old_text[:-1]
					self.text = new_text
					toast('There is a max of 30 tags')
		else:
			old_text = self.text
			new_text = old_text[:-1]
			self.text = new_text
			toast('Maximum Characters is 25')
	def on_text_validate(self):
		if len(running_app.posting_tags)<=30:
			typed_text = self.text
			tag_text = typed_text.replace(' ', '')
			if ('#'+tag_text) in running_app.posting_tags:
				toast('You have already tagged this hastag')
			else:
				self.text = ''
				if tag_text!='':
					new_tag_text =('#'+tag_text)
					self.layout.add_widget(ChosenTagsCard(text = new_tag_text))
					running_app.posting_tags.append(new_tag_text)
		else:
			toast('There is a max of 30 tags')

class ChosenTagsCard(BoxLayout):
	text = StringProperty('')
class SearchTextInput(TextInput):
	previous_text = StringProperty('')
	def on_text(instance,self, value):
		if (len(self.text))<30:
			for i in self.text:
				if i not in acceptaple_char and (i.lower()) not in acceptaple_char:
					old_text = self.text
					new_text = old_text.replace(i, '')
					self.text= new_text
					toast(str(i+' is not allowed'))
		else:
			old_text = self.text
			new_text = old_text[:-1]
			self.text = new_text
			toast('Maximum Characters is 30')








running_app = Pulsar()
running_app.run()
