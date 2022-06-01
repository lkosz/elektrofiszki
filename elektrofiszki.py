#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from gtts.lang import tts_langs
import sys, threading, time, numpy as np, datetime, os, traceback, warnings, ujson as json, glob, random, hashlib, argparse, colorama
from gtts import gTTS
from collections import deque

lvl = {
  '0': {
    'incr_t': 0,
    'incr': '1',
    'decr': '0',
  },
  '1': {
    'incr_t': 300, #5min
    'incr': '2',
    'decr': '0',
  },
  '2': {
    'incr_t': 900, #15min
    'incr': '3',
    'decr': '0',
  },
  '3': {
    'incr_t': 1*24*3600, # 1d
    'incr': '4',
    'decr': '0',
  },
  '4': {
    'incr_t': 2*24*3600, #2d
    'incr': '5',
    'decr': '2',
  },
  '5': {
    'incr_t': 3*24*3600, #3d
    'incr': '6',
    'decr': '2',
  },
  '6': {
    'incr_t': 7*24*3600, #7d
    'incr': '7',
    'decr': '3',
  },
  '7': {
    'incr_t': 7*24*3600, #7d
    'incr': '8',
    'decr': '3',
  },
  '8': {
    'incr_t': 14*24*3600, #14d
    'incr': '9',
    'decr': '4',
  },
  '9': {
    'incr_t': 14*24*3600, #14d
    'incr': '10',
    'decr': '4',
  },
  '10': {
    'incr_t': 30*24*3600, #30d
    'incr': '11',
    'decr': '5',
  },
  '11': {
    'incr_t': 30*24*3600, #30d
    'incr': '12',
    'decr': '5',
  },
  '12': {
    'incr_t': 60*24*3600, #60d
    'incr': '13',
    'decr': '5',
  },
  '13': {
    'incr_t': 120*24*3600, #120d
    'incr': '14',
    'decr': '5',
  },
  '14': {
    'incr_t': 240*24*3600, #240d
    'incr': '15',
    'decr': '5',
  },
  '15': {
    'incr_t': 300*24*3600, #300d
    'incr': '15',
    'decr': '5',
  },
}

q_speech = deque(maxlen=10)
kill_thread = False

#############################################################################################

#self, txt, lang, slow
def f_txt_to_speech():
  global kill_thread, q_speech

  while kill_thread == False:
    while kill_thread == False and not q_speech:
      time.sleep(0.1)
    if kill_thread:
      break

    item = q_speech.popleft()

    filename = str(hashlib.sha384(str(item['txt']).encode()).hexdigest())
    filename_full_path = 'elektrofiszki_audio/' + filename + '.mp3'

    if not os.path.isdir('elektrofiszki_audio'):
      os.mkdir('elektrofiszki_audio')

    if not os.path.isfile(filename_full_path):
      tts = gTTS('\n'.join([s + '.' for s in item['txt']]), lang=item['lang'], slow=False)
      tts.save(filename_full_path)

    if item['slow']:
      os.system('mpv --speed=0.8 --really-quiet ' + filename_full_path)
    else:
      os.system('mpv --really-quiet ' + filename_full_path)


#############################################################################################

class Window(QWidget):
  global lvl, q_speech

  def __init__(self):
    QWidget.__init__(self)
    self.win = QStackedWidget()

    self.winlayout = QHBoxLayout()
    self.winlayout.addWidget(self.win)
    self.setLayout(self.winlayout)

    self.winUI1()
    self.winUI2()
    self.winUI3()
    self.winUI4()
    self.winUI5()


#############################################################################################

  def winUI1(self):
    self.headline = QFont('SansSerif', 11, QFont.Bold)

    self.label1 = QLabel("Menu")
    self.label1.setFont(self.headline)

    self.create_dict = QPushButton('Create new', self)
    self.create_dict.clicked.connect(self.f_create_dict)
    self.open_dict = QPushButton('Open', self)
    self.open_dict.clicked.connect(self.f_open_dict)



    self.win1 = QWidget()
    layout2 = QVBoxLayout()
    layout2.addStretch()
    layout2.addWidget(self.label1)
    layout = QHBoxLayout()
    layout.addWidget(self.create_dict)
    layout.addWidget(self.open_dict)
    layout2.addLayout(layout)
    layout2.addStretch()

    self.win1.setLayout(layout2)
    self.win.addWidget(self.win1)

#############################################################################################

  def winUI2(self):
    self.headline = QFont('SansSerif', 11, QFont.Bold)

    self.label2 = QLabel("Create new")
    self.label2.setFont(self.headline)

    self.main_menu2 = QPushButton('Main menu', self)
    self.main_menu2.clicked.connect(self.f_main_menu)

    langs_list = sorted(list(tts_langs().values()))

    self.lang1_label = QLabel("Lang 1:")
    self.lang1_list_box = QComboBox(self)
    self.lang1_list_box.addItems(langs_list)

    self.lang2_label = QLabel("Lang 2:")
    self.lang2_list_box = QComboBox(self)
    self.lang2_list_box.addItems(langs_list)

    self.create_dict_do = QPushButton('Create', self)
    self.create_dict_do.clicked.connect(self.f_create_dict_do)

    self.label_create = QLabel("Choose language and click 'Create'")

    self.win2 = QWidget()
    layout = QVBoxLayout()

    layout2 = QHBoxLayout()
    layout2.addWidget(self.main_menu2)
    layout2.addStretch()
    layout2.addWidget(self.label2)
    layout2.addStretch()


    layout3 = QHBoxLayout()
    layout3.addStretch()
    layout3.addWidget(self.label_create)
    layout3.addWidget(self.lang1_label)
    layout3.addWidget(self.lang1_list_box)
    layout3.addWidget(self.lang2_label)
    layout3.addWidget(self.lang2_list_box)
    layout3.addWidget(self.create_dict_do)
    layout3.addStretch()

    layout.addStretch()
    layout.addLayout(layout2)
    layout.addLayout(layout3)
    layout.addStretch()

    self.win2.setLayout(layout)
    self.win.addWidget(self.win2)

#############################################################################################

  def winUI3(self):
    self.headline = QFont('SansSerif', 11, QFont.Bold)

    self.label3 = QLabel("Open dict")
    self.label3.setFont(self.headline)

    self.main_menu3 = QPushButton('Main menu', self)
    self.main_menu3.clicked.connect(self.f_main_menu)

    self.label_open = QLabel("Choose dictionary and direction")

    self.dicts_list_box = QComboBox(self)
    self.dicts_list_box.addItems(['NULL'])
    self.dicts_list_box.currentIndexChanged.connect(self.f_reload_dicts_direction_box)

    self.dicts_direction_box = QComboBox(self)
    self.dicts_direction_box.addItems(['NULL'])

    self.open_dict_ask = QPushButton('Open and ask', self)
    self.open_dict_ask.clicked.connect(self.f_open_dict_ask)

    self.open_dict_edit = QPushButton('Open and edit', self)
    self.open_dict_edit.clicked.connect(self.f_open_dict_edit)

    self.win3 = QWidget()
    layout2 = QHBoxLayout()
    layout2.addWidget(self.main_menu3)
    layout2.addStretch()
    layout2.addWidget(self.label3)
    layout2.addStretch()

    layout3 = QHBoxLayout()
    layout3.addStretch()
    layout3.addWidget(self.label_open)
    layout3.addWidget(self.dicts_list_box)
    layout3.addWidget(self.dicts_direction_box)
    layout3.addWidget(self.open_dict_ask)
    layout3.addWidget(self.open_dict_edit)
    layout3.addStretch()

    layout = QVBoxLayout()
    layout.addStretch()
    layout.addLayout(layout2)
    layout.addLayout(layout3)
    layout.addStretch()

    self.win3.setLayout(layout)
    self.win.addWidget(self.win3)

#############################################################################################

  def winUI4(self):
    self.headline = QFont('SansSerif', 11, QFont.Bold)

    self.main_menu4 = QPushButton('Main menu', self)
    self.main_menu4.clicked.connect(self.f_main_menu)

    self.label4 = QLabel("Edit dictionary")
    self.label4.setFont(self.headline)

    self.lang1_words = QPlainTextEdit()
    self.lang2_words = QPlainTextEdit()

    self.new_word = QPushButton('New word', self)
    self.new_word.clicked.connect(self.f_new_word)

    self.save_new_word = QPushButton('Save new word', self)
    self.save_new_word.clicked.connect(self.f_save_new_word)

    self.win4_output_msg = QLabel("NULL")
    self.lang1_name = QLabel("NULL")
    self.lang2_name = QLabel("NULL")

    self.lang1_search_txt = QLineEdit()
    self.lang2_search_txt = QLineEdit()
    self.lang1_search_butt = QPushButton('Search', self)
    self.lang1_search_butt.clicked.connect(self.f_search_lang1)
    self.lang2_search_butt = QPushButton('Search', self)
    self.lang2_search_butt.clicked.connect(self.f_search_lang2)


    self.dict_position = QLabel("Dict position")

    self.dict_item_no = QSpinBox()
    self.dict_item_no.setValue(-1)
    self.dict_item_no.valueChanged.connect(self.f_dict_item_no)

    self.replace_dict_item = QPushButton('replace', self)
    self.replace_dict_item.clicked.connect(self.f_replace)




    layout2 = QHBoxLayout()
    layout2.addWidget(self.main_menu4)
    layout2.addStretch()
    layout2.addWidget(self.label4)
    layout2.addStretch()

    layout3 = QHBoxLayout()
    layout3.addStretch()
    layout3.addWidget(self.new_word)
    layout3.addWidget(self.save_new_word)
    layout3.addWidget(self.dict_position)
    layout3.addWidget(self.dict_item_no)
    layout3.addWidget(self.replace_dict_item)
    layout3.addStretch()



    layout4a = QVBoxLayout()
    layout4aa = QHBoxLayout()
    layout4aa.addStretch()
    layout4aa.addWidget(self.lang1_name)
    layout4aa.addStretch()
    layout4a.addLayout(layout4aa)
    layout4a.addWidget(self.lang1_words)
    layout4ab = QHBoxLayout()
    layout4ab.addWidget(self.lang1_search_txt)
    layout4ab.addWidget(self.lang1_search_butt)
    layout4a.addLayout(layout4ab)

    layout4b = QVBoxLayout()
    layout4ba = QHBoxLayout()
    layout4ba.addStretch()
    layout4ba.addWidget(self.lang2_name)
    layout4ba.addStretch()
    layout4b.addLayout(layout4ba)
    layout4b.addWidget(self.lang2_words)
    layout4bb = QHBoxLayout()
    layout4bb.addWidget(self.lang2_search_txt)
    layout4bb.addWidget(self.lang2_search_butt)
    layout4b.addLayout(layout4bb)

    layout4 = QHBoxLayout()
    layout4.addStretch()
    layout4.addLayout(layout4a)
    layout4.addLayout(layout4b)
    layout4.addStretch()

    layout5 = QHBoxLayout()
    layout5.addStretch()
    layout5.addWidget(self.win4_output_msg)
    layout5.addStretch()


    self.win4 = QWidget()
    layout = QVBoxLayout()
    layout.addStretch()
    layout.addLayout(layout2)
    layout.addLayout(layout3)
    layout.addLayout(layout4)
    layout.addLayout(layout5)
    layout.addStretch()

    self.win4.setLayout(layout)
    self.win.addWidget(self.win4)

#############################################################################################

  def winUI5(self):
    self.headline = QFont('SansSerif', 11, QFont.Bold)

    self.main_menu5 = QPushButton('Main menu', self)
    self.main_menu5.clicked.connect(self.f_main_menu)

    self.question_words = QPlainTextEdit()
    q_font = self.question_words.font()
    q_font.setPointSize(16)
    self.question_words.setFont(q_font)



    self.answer_words = QLineEdit()
    self.answer_words.returnPressed.connect(self.f_check_answer)
    a_font = self.question_words.font()
    a_font.setPointSize(16)
    self.answer_words.setFont(a_font)

    self.question_label = QLabel("NULL")
    self.question_label.setFont(self.headline)
    self.answer_label = QLabel("NULL")
    self.answer_label.setFont(self.headline)

    self.check_answer = QPushButton('Check', self)
    self.check_answer.clicked.connect(self.f_check_answer)

    self.read_question = QPushButton('Read', self)
    self.read_question.clicked.connect(self.f_read_question)

    self.add_this_response = QPushButton('Add this response', self)
    self.add_this_response.clicked.connect(self.f_add_this_response)

    self.win5_msg = QLabel("-")
    self.win5_msg.setFont(self.headline)


    layout2 = QHBoxLayout()
    layout2.addStretch()
    layout2.addWidget(self.question_label)
    layout2.addWidget(self.question_words)
    layout2.addWidget(self.read_question)
    layout2.addStretch()

    layout3 = QHBoxLayout()
    layout3.addStretch()
    layout3.addWidget(self.answer_label)
    layout3.addWidget(self.answer_words)
    layout3.addWidget(self.check_answer)
    layout3.addWidget(self.add_this_response)
    layout3.addStretch()

    layout4 = QHBoxLayout()
    layout4.addWidget(self.main_menu5)
    layout4.addStretch()

    layout5 = QHBoxLayout()
    layout5.addStretch()
    layout5.addWidget(self.win5_msg)
    layout5.addStretch()

    layout = QVBoxLayout()
    layout.addStretch()
    layout.addLayout(layout4)
    layout.addLayout(layout2)
    layout.addLayout(layout3)
    layout.addLayout(layout5)
    layout.addStretch()

    self.win5 = QWidget()
    self.win5.setLayout(layout)
    self.win.addWidget(self.win5)

#############################################################################################

  def f_add_this_response(self):
    choosen_dict = self.dicts_list_box.currentText()
    choosen_direction = self.dicts_direction_box.currentText()
    f = open(choosen_dict, 'r')
    data = json.loads(f.read())
    f.close()
    l1 = data['lang1_long']
    l2 = data['lang2_long']
    if choosen_direction == l1 + ' TO ' + l2:
      q_lang_verb = 'lang1'
      q_lang_verb_answer = 'lang2'
      q_lang_timestamp_verb = 'l1_to_l2_timestamp'
      q_lang_level_verb = 'l1_to_l2_level'
    else:
      q_lang_verb = 'lang2'
      q_lang_verb_answer = 'lang1'
      q_lang_timestamp_verb = 'l2_to_l1_timestamp'
      q_lang_level_verb = 'l2_to_l1_level'

    question = self.question_words.toPlainText().split('\n')
    index = None

    for i in range(len(data['data'])):
      if data['data'][i][q_lang_verb] == question:
        index = i
        break

    if index == None:
      print("Internal error - can't find asked question in json")
      return

    data['data'][index][q_lang_verb_answer].append(self.answer_words.text())

    f = open(choosen_dict, 'w', encoding='utf8')
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
    f.close()

    self.f_check_answer()


  def f_check_answer(self):
    global lvl

    choosen_dict = self.dicts_list_box.currentText()
    choosen_direction = self.dicts_direction_box.currentText()
    f = open(choosen_dict, 'r')
    data = json.loads(f.read())
    f.close()
    l1 = data['lang1_long']
    l2 = data['lang2_long']
    if choosen_direction == l1 + ' TO ' + l2:
      q_lang_verb = 'lang1'
      q_lang_verb_answer = 'lang2'
      q_lang_timestamp_verb = 'l1_to_l2_timestamp'
      q_lang_level_verb = 'l1_to_l2_level'
    else:
      q_lang_verb = 'lang2'
      q_lang_verb_answer = 'lang1'
      q_lang_timestamp_verb = 'l2_to_l1_timestamp'
      q_lang_level_verb = 'l2_to_l1_level'

    question = self.question_words.toPlainText().split('\n')
    index = None

    for i in range(len(data['data'])):
      if data['data'][i][q_lang_verb] == question:
        index = i
        break

    if index == None:
      print("Internal error - can't find asked question in json")
      return

    if self.answer_words.text() in data['data'][index][q_lang_verb_answer]:
      self.f_read_answer(slow=False)
      self.win5_msg.setText('-')
      data['data'][index][q_lang_level_verb] = lvl[str(data['data'][index][q_lang_level_verb])]['incr']
      ok = True
    else:
      self.win5_msg.setText('Wrong answer. Write one of correct answer: ' + ';'.join(data['data'][index][q_lang_verb_answer]))
      self.f_read_question(slow=False)
      self.f_read_answer(slow=False)
      data['data'][index][q_lang_level_verb] = lvl[str(data['data'][index][q_lang_level_verb])]['decr']
      ok = False

    data['data'][index][q_lang_timestamp_verb] = int(time.time()) + int(lvl[str(data['data'][index][q_lang_level_verb])]['incr_t'])

    f = open(choosen_dict, 'w', encoding='utf8')
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
    f.close()

    if ok:
      self.f_ask_a_question()


  def f_read_answer(self, slow=True):
    global q_speech

    choosen_dict = self.dicts_list_box.currentText()
    choosen_direction = self.dicts_direction_box.currentText()

    f = open(choosen_dict, 'r')
    data = json.loads(f.read())
    f.close()

    l1 = data['lang1_long']
    l2 = data['lang2_long']
    if choosen_direction == l1 + ' TO ' + l2:
      q_lang_verb = 'lang1'
      a_lang_verb = 'lang2'
    else:
      q_lang_verb = 'lang2'
      a_lang_verb = 'lang1'

    question = self.question_words.toPlainText().split('\n')
    index = None

    for i in range(len(data['data'])):
      if data['data'][i][q_lang_verb] == question:
        index = i
        break

    if index == None:
      print("Internal error - can't find asked question in json")
      return

    item = {
      'txt': data['data'][index][a_lang_verb],
      'lang': data[a_lang_verb],
      'slow': slow,
    }
    q_speech.append(item)

  def f_read_question(self, slow=True):
    global q_speech

    choosen_dict = self.dicts_list_box.currentText()
    choosen_direction = self.dicts_direction_box.currentText()

    f = open(choosen_dict, 'r')
    data = json.loads(f.read())
    f.close()

    l1 = data['lang1_long']
    l2 = data['lang2_long']
    if choosen_direction == l1 + ' TO ' + l2:
      q_lang_verb = 'lang1'
    else:
      q_lang_verb = 'lang2'

    item = {
      'txt': self.question_words.toPlainText().split('\n'),
      'lang': data[q_lang_verb],
      'slow': slow,
    }
    q_speech.append(item)

  def f_ask_a_question(self):
    choosen_dict = self.dicts_list_box.currentText()
    choosen_direction = self.dicts_direction_box.currentText()
    f = open(choosen_dict, 'r')
    data = json.loads(f.read())
    f.close()
    l1 = data['lang1_long']
    l2 = data['lang2_long']
    if choosen_direction == l1 + ' TO ' + l2:
      self.question_label.setText(l1)
      self.answer_label.setText(l2)
      q_lang_verb = 'lang1'
      q_lang_timestamp_verb = 'l1_to_l2_timestamp'
    else:
      self.question_label.setText(l2)
      self.answer_label.setText(l1)
      q_lang_verb = 'lang2'
      q_lang_timestamp_verb = 'l2_to_l1_timestamp'

    available_questions = []
    timestamp = int(time.time())

    for i in data['data']:
      if i[q_lang_timestamp_verb] <= timestamp:
        available_questions.append(i)

    if len(available_questions) == 0:
      self.answer_words.clear()
      self.answer_words.setFocus()
      self.question_words.clear()
      self.question_words.setReadOnly(True)
      self.win5_msg.setText('Currently no new words to ask. Try again later')
      return

    question = random.choice(available_questions)
    self.question_words.setPlainText('\n'.join(question[q_lang_verb]))
    self.question_words.setReadOnly(True)
    self.f_read_question(slow=False)
    self.answer_words.clear()
    self.answer_words.setFocus()
    self.win5_msg.setText( '(' + str(len(available_questions)) + ') Write one of answer which exists in dict and hit enter or check')


  def f_main_menu(self):
    self.win.setCurrentIndex(0)

  def f_create_dict(self):
    self.win.setCurrentIndex(1)

  def f_replace(self):
    choosen_dict = self.dicts_list_box.currentText()
    choosen_direction = self.dicts_direction_box.currentText()
    value = self.dict_item_no.value()

    if value < 0:
      return

    f = open(choosen_dict, 'r')
    data = json.loads(f.read())
    f.close()
    tab_lang1 = self.lang1_words.toPlainText().split('\n')
    tab_lang2 = self.lang2_words.toPlainText().split('\n')

    data['data'][value]['lang1'] = tab_lang1
    data['data'][value]['lang2'] = tab_lang2

    f = open(choosen_dict, 'w', encoding='utf8')
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
    f.close()

    self.win4_output_msg.setText('Replaced')



  def f_dict_item_no(self):
    choosen_dict = self.dicts_list_box.currentText()
    choosen_direction = self.dicts_direction_box.currentText()
    value = self.dict_item_no.value()

    if value < 0:
      return

    f = open(choosen_dict, 'r')
    data = json.loads(f.read())
    f.close()

    self.lang1_words.setPlainText('\n'.join(data['data'][value]['lang1']))
    self.lang2_words.setPlainText('\n'.join(data['data'][value]['lang2']))
    self.win4_output_msg.setText('Found')
    self.lang1_words.setReadOnly(False)
    self.lang2_words.setReadOnly(False)

  def f_open_dict(self):
    files = sorted(glob.glob('elektrofiszki*.json'))
    if len(files) > 0:
      self.dicts_list_box.clear()
      self.dicts_list_box.addItems(files)
      self.f_reload_dicts_direction_box()
    self.win.setCurrentIndex(2)
    self.dict_item_no.setValue(-1)

  def f_search_lang1(self):
    choosen_dict = self.dicts_list_box.currentText()
    choosen_direction = self.dicts_direction_box.currentText()
    search_text = self.lang1_search_txt.text()

    f = open(choosen_dict, 'r')
    data = json.loads(f.read())
    f.close()

    j=0
    for i in data['data']:
      if search_text in i['lang1']:
        self.lang1_words.setPlainText('\n'.join(i['lang1']))
        self.lang2_words.setPlainText('\n'.join(i['lang2']))
        self.win4_output_msg.setText('Found')
        self.lang1_words.setReadOnly(False)
        self.lang2_words.setReadOnly(False)
        self.dict_item_no.setMinimum(-1)
        self.dict_item_no.setMaximum(len(data['data'])-1)
        self.dict_item_no.setValue(j)
        return
      j+=1

    self.lang1_words.clear()
    self.lang2_words.clear()
    self.win4_output_msg.setText(search_text + ' not found')
    self.dict_item_no.setMaximum(-1)



  def f_search_lang2(self):
    choosen_dict = self.dicts_list_box.currentText()
    choosen_direction = self.dicts_direction_box.currentText()
    search_text = self.lang2_search_txt.text()

    f = open(choosen_dict, 'r')
    data = json.loads(f.read())
    f.close()

    j=0
    for i in data['data']:
      if search_text in i['lang2']:
        self.lang1_words.setPlainText('\n'.join(i['lang1']))
        self.lang2_words.setPlainText('\n'.join(i['lang2']))
        self.win4_output_msg.setText('Found')
        self.lang1_words.setReadOnly(False)
        self.lang2_words.setReadOnly(False)
        self.dict_item_no.setMinimum(-1)
        self.dict_item_no.setMaximum(len(data['data'])-1)
        self.dict_item_no.setValue(j)
        return
      j+=1

    self.lang1_words.clear()
    self.lang2_words.clear()
    self.win4_output_msg.setText(search_text + ' not found')
    self.dict_item_no.setMaximum(-1)


  def f_edit_dict(self):
    choosen_dict = self.dicts_list_box.currentText()
    self.win.setCurrentIndex(3)
    self.win4_output_msg.setText('Choose option first')
    self.lang1_words.setReadOnly(True)
    self.lang2_words.setReadOnly(True)
    self.lang1_words.clear()
    self.lang2_words.clear()

    f = open(choosen_dict, 'r')
    data = json.loads(f.read())
    f.close()

    self.dict_item_no.setMinimum(-1)
    self.dict_item_no.setMaximum(len(data['data'])-1)
    self.dict_item_no.setValue(-1)

    self.lang1_name.setText(data['lang1_long'])
    self.lang2_name.setText(data['lang2_long'])


  def f_new_word(self):
    self.lang1_words.clear()
    self.lang2_words.clear()
    self.lang1_words.setReadOnly(False)
    self.lang2_words.setReadOnly(False)
    self.win4_output_msg.setText('Add new words')
    self.dict_item_no.setValue(-1)
    self.dict_item_no.setMinimum(-1)
    self.dict_item_no.setMaximum(-1)

  def print_err(self, msg):
    print(colorama.Fore.RED + str(msg) + colorama.Style.RESET_ALL)

  def f_save_new_word(self, cli_mode = False, a_choosen_dict = None, a_lang1_short = None, a_lang2_short = None, a_lang1_words = None, a_lang2_words = None):

    if cli_mode:
      if a_choosen_dict == None:
        self.print_err('var a_choosen_dict is None')
        sys.exit(1)
      if a_lang1_short == None:
        self.print_err('var a_lang1_short is None')
        sys.exit(1)
      if a_lang2_short == None:
        self.print_err('var a_lang2_short is None')
        sys.exit(1)
      if a_lang1_words == None:
        self.print_err('var a_lang1_words is None')
        sys.exit(1)
      if a_lang2_words == None:
        self.print_err('var a_lang2_words is None')
        sys.exit(1)

      choosen_dict = a_choosen_dict
      tab_lang1 = a_lang1_words
      tab_lang2 = a_lang2_words

      if not os.path.isfile(choosen_dict):
        self.print_err(choosen_dict + ' does not exist!')
        sys.exit(1)
    else:
      choosen_dict = self.dicts_list_box.currentText()
      tab_lang1 = self.lang1_words.toPlainText().split('\n')
      tab_lang2 = self.lang2_words.toPlainText().split('\n')

    for i in range(len(tab_lang1)):
      if tab_lang1[i] == '':
        del tab_lang1[i]

    for i in range(len(tab_lang2)):
      if tab_lang2[i] == '':
        del tab_lang2[i]

    if len(tab_lang1) == 0 or len(tab_lang2) == 0:
      self.print_err('Missing words in at least one of text spaces')
      self.win4_output_msg.setText('Missing words in at least one of text spaces')
      return

    f = open(choosen_dict, 'r')
    data = json.loads(f.read())
    f.close()

    if cli_mode:
      if a_lang1_short != data['lang1']:
        self.print_err('lang1 name in dict is different than set in command line')
        sys.exit(1)
      if a_lang2_short != data['lang2']:
        self.print_err('lang2 name in dict is different than set in command line')
        sys.exit(1)

    for i in tab_lang1:
      for j in data['data']:
        if i in j['lang1']:
          if cli_mode:
            self.print_err('STOP! "' + i + '" already exists in dict')
            sys.exit(1)
          else:
           self.win4_output_msg.setText('\033[91m STOP! "' + i + '" already exists in dict')
           return

    for i in tab_lang2:
      for j in data['data']:
        if i in j['lang2']:
          if cli_mode:
            self.print_err('STOP! "' + i + '" already exists in dict')
            sys.exit(1)
          else:
           self.win4_output_msg.setText('STOP! ' + i + ' already exists in dict')
           return

    item = {
      'lang1': tab_lang1,
      'lang2': tab_lang2,
      'l1_to_l2_level': "0",
      'l2_to_l1_level': "0",
      'l1_to_l2_timestamp': 0,
      'l2_to_l1_timestamp': 0,
    }
    data['data'].append(item)

    f = open(choosen_dict, 'w', encoding='utf8')
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
    f.close()

    if cli_mode:
      print('OK')
    else:
      self.dict_item_no.setMinimum(-1)
      self.dict_item_no.setMaximum(len(data['data'])-1)
      self.dict_item_no.setValue(len(data['data'])-1)
      self.win4_output_msg.setText('Saved. Choose next option')




  def f_reload_dicts_direction_box(self):
    choosen_dict = self.dicts_list_box.currentText()
    if choosen_dict in ['NULL', '']:
      return
    f = open(choosen_dict, 'r')
    data = json.loads(f.read())
    f.close()
    l1 = data['lang1_long']
    l2 = data['lang2_long']
    items = [l1 + ' TO ' + l2, l2 + ' TO ' + l1]
    self.dicts_direction_box.clear()
    self.dicts_direction_box.addItems(items)

  def f_open_dict_ask(self):
    choosen_dict = self.dicts_list_box.currentText()
    choosen_direction = self.dicts_direction_box.currentText()

    if choosen_dict in ['', 'NULL'] or choosen_direction in ['', 'NULL']:
      print("Error! No dictionary files found. Go to main menu and create new.")
      self.label_open.setText("Error! No dictionary files found. Go to main menu and create new.")
      return

    self.win.setCurrentIndex(4)
    self.f_ask_a_question()

  def f_open_dict_edit(self):
    choosen_dict = self.dicts_list_box.currentText()
    choosen_direction = self.dicts_direction_box.currentText()

    if choosen_dict in ['', 'NULL'] or choosen_direction in ['', 'NULL']:
      print("Error! No dictionary files found. Go to main menu and create new.")
      self.label_open.setText("Error! No dictionary files found. Go to main menu and create new.")
      return

    self.f_edit_dict()


  def f_create_dict_do(self):
    choosen_lang1 = self.lang1_list_box.currentText()
    choosen_lang2 = self.lang2_list_box.currentText()
    lang_list = tts_langs()
    lang1_code = None
    lang2_code = None
    for i in lang_list.keys():
      if lang_list[i] == choosen_lang1:
        lang1_code = i
      if lang_list[i] == choosen_lang2:
        lang2_code = i
      if lang1_code != None and lang2_code != None:
        break
    if lang1_code == None or lang2_code == None:
      print("Internal error! Can't find lang code")
      self.label_create.setText("Internal error!!! Can't find lang code")
      return

    if lang1_code == lang2_code:
      print("Error! Both langs are the same. Change it and try again")
      self.label_create.setText("Error! Both langs are the same. Change it and try again")
      return

    filename = 'elektrofiszki_' + lang1_code + '_' + lang2_code + '.json'
    if os.path.exists(filename):
      print("ERROR! Dict for this language already exists!")
      self.label_create.setText("ERROR! Dict for this language already exists!")
      return

    data = {
      'lang1_long': choosen_lang1,
      'lang1': lang1_code,
      'lang2_long': choosen_lang2,
      'lang2': lang2_code,
      'data': []
    }
    f = open(filename, 'w', encoding='utf8')
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
    f.close()
    self.label_create.setText("File created. Go to main menu and open.")


#############################################################################################
parser = argparse.ArgumentParser(description='Elektrofiszki CLI')
parser.add_argument('--cli_mode', action=argparse.BooleanOptionalAction,            help='turn on CLI mode')
parser.add_argument('--dict_file',  dest='dict_file', required=False, type=str,     help='name of json dict file')
parser.add_argument('--lang1_short',  dest='lang1_short', required=False, type=str, help='short lang1 name eg. pl, no')
parser.add_argument('--lang2_short',  dest='lang2_short', required=False, type=str, help='short lang2 name eg. pl, no')
parser.add_argument('--lang1_words',  dest='lang1_words', required=False, type=str, help='colon separated words for lang1')
parser.add_argument('--lang2_words',  dest='lang2_words', required=False, type=str, help='colon separated words for lang2')
args = parser.parse_args()

#############################################################################################


app = QApplication(sys.argv)
screen = Window()

if not args.cli_mode:

  thread_list = []

  t = threading.Thread(target=f_txt_to_speech)
  thread_list.append(t)

  for thread in thread_list:
      thread.start()

  screen.showMaximized()
  app.exec_()

  kill_thread = True

else:
  if not args.dict_file:
    screen.print_err('--dict_file required')
    sys.exit(1)
  if not args.lang1_short:
    screen.print_err('--lang1_short required')
    sys.exit(1)
  if not args.lang2_short:
    screen.print_err('--lang2_short required')
    sys.exit(1)
  if not args.lang1_words:
    screen.print_err('--lang1_words required')
    sys.exit(1)
  if not args.lang2_words:
    screen.print_err('--lang2_words required')
    sys.exit(1)

  lang1_words_arr = args.lang1_words.split(';')
  lang2_words_arr = args.lang2_words.split(';')

  screen.f_save_new_word(cli_mode=True, a_choosen_dict = args.dict_file, a_lang1_short = args.lang1_short, a_lang2_short = args.lang2_short, a_lang1_words = lang1_words_arr, a_lang2_words = lang2_words_arr)
