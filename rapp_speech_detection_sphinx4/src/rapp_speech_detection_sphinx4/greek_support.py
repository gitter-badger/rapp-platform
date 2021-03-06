#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright 2015 RAPP

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

    #http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# Authors: Athanassios Kintsakis, Aris Thallas, Manos Tsardoulias
# contact: akintsakis@issel.ee.auth.gr, aris.thallas@{iti.gr, gmail.com}, etsardou@iti.gr


import rospy
import sys
import re
import mmap

from global_parameters import GlobalParams
from rapp_exceptions import RappError
from english_support import *
from limited_vocabulary_creator import *
from rapp_tools import *

class GreekSupport(GlobalParams):

  def __init__(self):
    GlobalParams.__init__(self)

    #self.generic_sphinx_configuration = {}
    self.limited_sphinx_configuration = {}

    self.vocabulary = LimitedVocabularyCreator()
    # TODO: Split the rapp_sphinx4_java_libraries package into libraries and
    # language models
    # NOTE: This does not exist yet
    self.greek_dictionary = self.language_models_url + \
        "/englishPack/cmudict-en-us.dict"

    jar_path = ".:" + self.sphinx_jar_files_url + "/" + \
        self.sphinx_jar_file + ":" \
            + self.sphinx_package_url + "/src"

    # Grammar is dummy here..
    # NOTE: Fix this according to the generic Greek model
    self.generic_sphinx_configuration = { \
      'jar_path' : jar_path, \
      'configuration_path' : self.language_models_url + "/greekPack/default.config.xml", \
      'acoustic_model' : self.acoustic_models_url + "/acoustic_model/", \
      'grammar_name' : 'hello', \
      'grammar_folder' : self.language_models_url + "/greekPack/", \
      'dictionary' : self.language_models_url +  "/englishPack/cmudict-en-us.dict", \
      'language_model' : self.language_models_url + "/englishPack/en-us.lm.bin", \
      'grammar_disabled' : True
      }

    self._english_support = EnglishSupport()
    # Open the generic english dictionary file
    # NOTE: Fix this according to the Greek generic dictionary
    #try:
      #self.english_dict_file = open(self.english_dictionary, 'r')
    #except IOError:
      #print "English dictionary could not be opened!"
    # Create a mapping of the file
    #self.english_dict_mapping = mmap.mmap(self.english_dict_file.fileno(), 0, \
        #access = mmap.ACCESS_READ)

    self.configureLetters()

  def configureLetters(self):

    self.f_base_pre = [u'π', u'τ', u'κ', u'θ', u'χ', u'σ', u'ξ', u'ψ']
    self.f_base = []
    for l in self.f_base_pre:
      self.f_base.append(l.encode('utf-8'))

    self.v_base_pre = [u'δ', u'γ', u'ζ', u'λ', u'ρ', u'μ', u'ν', u'α', u'ά', u'ε',\
        u'έ', u'η', u'ή', u'ι', u'ί', u'ϊ', u'ΐ', u'ο', u'ό', u'υ', u'ύ', u'ϋ'\
        u'ΰ', u'ω', u'ώ']
    self.v_base = []
    for l in self.v_base_pre:
      self.v_base.append(l.encode('utf-8'))

    self.capital_letters = {}
    self.capital_letters[(u'Α').encode('utf-8')] = (u'α').encode('utf-8')
    self.capital_letters[(u'Ά').encode('utf-8')] = (u'ά').encode('utf-8')
    self.capital_letters[(u'Β').encode('utf-8')] = (u'β').encode('utf-8')
    self.capital_letters[(u'Γ').encode('utf-8')] = (u'γ').encode('utf-8')
    self.capital_letters[(u'Δ').encode('utf-8')] = (u'δ').encode('utf-8')
    self.capital_letters[(u'Ε').encode('utf-8')] = (u'ε').encode('utf-8')
    self.capital_letters[(u'Έ').encode('utf-8')] = (u'έ').encode('utf-8')
    self.capital_letters[(u'Ζ').encode('utf-8')] = (u'ζ').encode('utf-8')
    self.capital_letters[(u'Η').encode('utf-8')] = (u'η').encode('utf-8')
    self.capital_letters[(u'Ή').encode('utf-8')] = (u'ή').encode('utf-8')
    self.capital_letters[(u'Θ').encode('utf-8')] = (u'θ').encode('utf-8')
    self.capital_letters[(u'Ι').encode('utf-8')] = (u'ι').encode('utf-8')
    self.capital_letters[(u'Ί').encode('utf-8')] = (u'ί').encode('utf-8')
    self.capital_letters[(u'Ϊ').encode('utf-8')] = (u'ϊ').encode('utf-8')
    self.capital_letters[(u'Κ').encode('utf-8')] = (u'κ').encode('utf-8')
    self.capital_letters[(u'Λ').encode('utf-8')] = (u'λ').encode('utf-8')
    self.capital_letters[(u'Μ').encode('utf-8')] = (u'μ').encode('utf-8')
    self.capital_letters[(u'Ν').encode('utf-8')] = (u'ν').encode('utf-8')
    self.capital_letters[(u'Ξ').encode('utf-8')] = (u'ξ').encode('utf-8')
    self.capital_letters[(u'Ο').encode('utf-8')] = (u'ο').encode('utf-8')
    self.capital_letters[(u'Ό').encode('utf-8')] = (u'ό').encode('utf-8')
    self.capital_letters[(u'Π').encode('utf-8')] = (u'π').encode('utf-8')
    self.capital_letters[(u'Ρ').encode('utf-8')] = (u'ρ').encode('utf-8')
    self.capital_letters[(u'Σ').encode('utf-8')] = (u'σ').encode('utf-8')
    self.capital_letters[(u'Τ').encode('utf-8')] = (u'τ').encode('utf-8')
    self.capital_letters[(u'Υ').encode('utf-8')] = (u'γ').encode('utf-8')
    self.capital_letters[(u'Ύ').encode('utf-8')] = (u'ύ').encode('utf-8')
    self.capital_letters[(u'Ϋ').encode('utf-8')] = (u'ϋ').encode('utf-8')
    self.capital_letters[(u'Φ').encode('utf-8')] = (u'φ').encode('utf-8')
    self.capital_letters[(u'Χ').encode('utf-8')] = (u'χ').encode('utf-8')
    self.capital_letters[(u'Ψ').encode('utf-8')] = (u'ψ').encode('utf-8')
    self.capital_letters[(u'Ω').encode('utf-8')] = (u'ω').encode('utf-8')
    self.capital_letters[(u'Ώ').encode('utf-8')] = (u'ώ').encode('utf-8')

    self.phonems = {}
    self.phonems[(u'ου').encode('utf-8')] = 'UW '
    self.phonems[(u'ού').encode('utf-8')] = 'UW '
    self.phonems[(u'μπ').encode('utf-8')] = 'B '
    self.phonems[(u'ντ').encode('utf-8')] = 'D '
    self.phonems[(u'γκ').encode('utf-8')] = 'G ' #?
    self.phonems[(u'γγ').encode('utf-8')] = 'G ' #?
    self.phonems[(u'τσ').encode('utf-8')] = 'CH ' #?
    self.phonems[(u'τζ').encode('utf-8')] = 'JH ' #?
    self.phonems[(u'σσ').encode('utf-8')] = 'S ' #?
    self.phonems[(u'κκ').encode('utf-8')] = 'K '
    self.phonems[(u'ββ').encode('utf-8')] = 'V '
    self.phonems[(u'λλ').encode('utf-8')] = 'L '
    self.phonems[(u'μμ').encode('utf-8')] = 'M '
    self.phonems[(u'νν').encode('utf-8')] = 'N '
    self.phonems[(u'ππ').encode('utf-8')] = 'P '
    self.phonems[(u'ρρ').encode('utf-8')] = 'R '
    self.phonems[(u'ττ').encode('utf-8')] = 'T '

    self.two_digit_letters = {}
    self.two_digit_letters[(u'αι').encode('utf-8')] = 'EH '
    self.two_digit_letters[(u'αί').encode('utf-8')] = 'EH '
    self.two_digit_letters[(u'ει').encode('utf-8')] = 'IH '
    self.two_digit_letters[(u'εί').encode('utf-8')] = 'IH '
    self.two_digit_letters[(u'οι').encode('utf-8')] = 'IH '
    self.two_digit_letters[(u'οί').encode('utf-8')] = 'IH '
    self.two_digit_letters[(u'υι').encode('utf-8')] = 'IH '
    self.two_digit_letters[(u'υί').encode('utf-8')] = 'IH '

    self.special_two_digit_letters = []
    self.special_two_digit_letters.append((u'αυ').encode('utf-8'))
    self.special_two_digit_letters.append((u'αύ').encode('utf-8'))
    self.special_two_digit_letters.append((u'ευ').encode('utf-8'))
    self.special_two_digit_letters.append((u'εύ').encode('utf-8'))
    self.special_two_digit_letters_v = {}
    self.special_two_digit_letters_v[(u'αυ').encode('utf-8')] = (u'αβ').encode('utf-8')
    self.special_two_digit_letters_v[(u'αύ').encode('utf-8')] = (u'άβ').encode('utf-8')
    self.special_two_digit_letters_v[(u'ευ').encode('utf-8')] = (u'εβ').encode('utf-8')
    self.special_two_digit_letters_v[(u'εύ').encode('utf-8')] = (u'έβ').encode('utf-8')
    self.special_two_digit_letters_f = {}
    self.special_two_digit_letters_f[(u'αυ').encode('utf-8')] = (u'αφ').encode('utf-8')
    self.special_two_digit_letters_f[(u'αύ').encode('utf-8')] = (u'άφ').encode('utf-8')
    self.special_two_digit_letters_f[(u'ευ').encode('utf-8')] = (u'εφ').encode('utf-8')
    self.special_two_digit_letters_f[(u'εύ').encode('utf-8')] = (u'έφ').encode('utf-8')

    self.all_special_two_digit_letters = {}
    for tdl in self.special_two_digit_letters:
      for fb in self.f_base:
        self.all_special_two_digit_letters[tdl + fb] = \
            self.special_two_digit_letters_f[tdl] + fb
    for tdl in self.special_two_digit_letters:
      for vb in self.v_base:
        self.all_special_two_digit_letters[tdl + vb] = \
            self.special_two_digit_letters_v[tdl] + vb

    self.s_specific_rules = {}
    self.s_specific_rules[(u'σγ').encode('utf-8')] = 'Z W '
    self.s_specific_rules[(u'σβ').encode('utf-8')] = 'Z V '
    self.s_specific_rules[(u'σδ').encode('utf-8')] = 'Z DH '
    self.s_specific_rules[(u'σμ').encode('utf-8')] = 'Z M '
    self.s_specific_rules[(u'σν').encode('utf-8')] = 'Z N '
    self.s_specific_rules[(u'σλ').encode('utf-8')] = 'Z L '
    self.s_specific_rules[(u'σρ').encode('utf-8')] = 'Z R '
    self.s_specific_rules[(u'σμπ').encode('utf-8')] = 'Z B '
    self.s_specific_rules[(u'σντ').encode('utf-8')] = 'Z D '

    self.letters = {}
    self.letters[(u'α').encode('utf-8')] = 'AA ' # when AE?
    self.letters[(u'ά').encode('utf-8')] = 'AA '
    self.letters[(u'β').encode('utf-8')] = 'V '
    self.letters[(u'γ').encode('utf-8')] = 'W '
    self.letters[(u'δ').encode('utf-8')] = 'DH '
    self.letters[(u'ε').encode('utf-8')] = 'EH '
    self.letters[(u'έ').encode('utf-8')] = 'EH '
    self.letters[(u'ζ').encode('utf-8')] = 'Z '
    self.letters[(u'η').encode('utf-8')] = 'IH '
    self.letters[(u'ή').encode('utf-8')] = 'IH '
    self.letters[(u'θ').encode('utf-8')] = 'TH '
    self.letters[(u'ι').encode('utf-8')] = 'IH '
    self.letters[(u'ί').encode('utf-8')] = 'IH '
    self.letters[(u'ϊ').encode('utf-8')] = 'IH '
    self.letters[(u'ΐ').encode('utf-8')] = 'IH '
    self.letters[(u'κ').encode('utf-8')] = 'K '
    self.letters[(u'λ').encode('utf-8')] = 'L '
    self.letters[(u'μ').encode('utf-8')] = 'M '
    self.letters[(u'ν').encode('utf-8')] = 'N '
    self.letters[(u'ξ').encode('utf-8')] = 'K S '
    self.letters[(u'ο').encode('utf-8')] = 'OW '
    self.letters[(u'ό').encode('utf-8')] = 'OW '
    self.letters[(u'π').encode('utf-8')] = 'P '
    self.letters[(u'ρ').encode('utf-8')] = 'R '
    self.letters[(u'σ').encode('utf-8')] = 'S '
    self.letters[(u'τ').encode('utf-8')] = 'T '
    self.letters[(u'υ').encode('utf-8')] = 'IH '
    self.letters[(u'ύ').encode('utf-8')] = 'IH '
    self.letters[(u'ϋ').encode('utf-8')] = 'IH '
    self.letters[(u'ΰ').encode('utf-8')] = 'IH '
    self.letters[(u'φ').encode('utf-8')] = 'F '
    self.letters[(u'χ').encode('utf-8')] = 'HH '
    self.letters[(u'ψ').encode('utf-8')] = 'P S '
    self.letters[(u'ω').encode('utf-8')] = 'OW '
    self.letters[(u'ώ').encode('utf-8')] = 'OW '
    self.letters[(u'ς').encode('utf-8')] = 'S '

    self.literal_letters = {}
    self.literal_letters[(u'α').encode('utf-8')] = 'a' # when AE?
    self.literal_letters[(u'ά').encode('utf-8')] = 'a\''
    self.literal_letters[(u'β').encode('utf-8')] = 'b'
    self.literal_letters[(u'γ').encode('utf-8')] = 'g'
    self.literal_letters[(u'δ').encode('utf-8')] = 'd'
    self.literal_letters[(u'ε').encode('utf-8')] = 'e'
    self.literal_letters[(u'έ').encode('utf-8')] = 'e\''
    self.literal_letters[(u'ζ').encode('utf-8')] = 'z'
    self.literal_letters[(u'η').encode('utf-8')] = 'h'
    self.literal_letters[(u'ή').encode('utf-8')] = 'h\''
    self.literal_letters[(u'θ').encode('utf-8')] = 'th'
    self.literal_letters[(u'ι').encode('utf-8')] = 'i'
    self.literal_letters[(u'ί').encode('utf-8')] = 'i\''
    self.literal_letters[(u'ϊ').encode('utf-8')] = 'i:'
    self.literal_letters[(u'ΐ').encode('utf-8')] = 'i\':'
    self.literal_letters[(u'κ').encode('utf-8')] = 'k'
    self.literal_letters[(u'λ').encode('utf-8')] = 'l'
    self.literal_letters[(u'μ').encode('utf-8')] = 'm'
    self.literal_letters[(u'ν').encode('utf-8')] = 'n'
    self.literal_letters[(u'ξ').encode('utf-8')] = 'ks'
    self.literal_letters[(u'ο').encode('utf-8')] = 'o'
    self.literal_letters[(u'ό').encode('utf-8')] = 'o\''
    self.literal_letters[(u'π').encode('utf-8')] = 'p'
    self.literal_letters[(u'ρ').encode('utf-8')] = 'r'
    self.literal_letters[(u'σ').encode('utf-8')] = 's'
    self.literal_letters[(u'ς').encode('utf-8')] = 's\''
    self.literal_letters[(u'τ').encode('utf-8')] = 't'
    self.literal_letters[(u'υ').encode('utf-8')] = 'u'
    self.literal_letters[(u'ύ').encode('utf-8')] = 'u\''
    self.literal_letters[(u'ϋ').encode('utf-8')] = 'u:'
    self.literal_letters[(u'ΰ').encode('utf-8')] = 'u\':'
    self.literal_letters[(u'φ').encode('utf-8')] = 'f'
    self.literal_letters[(u'χ').encode('utf-8')] = 'x'
    self.literal_letters[(u'ψ').encode('utf-8')] = 'ps'
    self.literal_letters[(u'ω').encode('utf-8')] = 'w'
    self.literal_letters[(u'ώ').encode('utf-8')] = 'w\''


  def transformWords(self, words):
    enhanced_words = {}
    englified_words = {}
    for word in words:
      initial_word = word
      rapp_print ("Initial word: " + initial_word)
      # transform capital letters
      for cap in self.capital_letters:
        initial_word = initial_word.replace(cap, self.capital_letters[cap])
      rapp_print ("Caps to small: " + initial_word)
      # fix english version of letters
      eng_w = initial_word
      for lit in self.literal_letters:
        eng_w = eng_w.replace(lit, self.literal_letters[lit])
      englified_words[eng_w] = word
      rapp_print ("Englified: " + eng_w)
      # check phonems
      for ph in self.phonems:
        initial_word = initial_word.replace(ph, self.phonems[ph])
      rapp_print ("Phonemes: " + initial_word)
      # check special two digit letters
      for stdl in self.all_special_two_digit_letters:
        initial_word = initial_word.replace(stdl, \
            self.all_special_two_digit_letters[stdl])
      rapp_print ("Special 2 digit letters: " + initial_word)
      # check two-digit letters
      for let in self.two_digit_letters:
        initial_word = initial_word.replace(let, self.two_digit_letters[let])
      rapp_print ("2 digit letters: " + initial_word)
      # check specific rules
      for sr in self.s_specific_rules:
        initial_word = initial_word.replace(sr, self.s_specific_rules[sr])
      rapp_print ("specific rules: " + initial_word)
      # check the rest of the letters
      for l in self.letters:
        initial_word = initial_word.replace(l, self.letters[l])
      rapp_print ("rest of letters: " + initial_word)

      enhanced_words[eng_w] = []
      temp = initial_word.split(' ')
      if len(temp) > 0:
        temp = temp[:-1]
      enhanced_words[eng_w] = temp

    return [enhanced_words, englified_words]

  def englify_words(self, words):
    englified_words = []
    for word in words:
      eng_w = word
      # First transform the Capitals
      for cap in self.capital_letters:
        eng_w = eng_w.replace(cap, self.capital_letters[cap])
      for lit in self.literal_letters:
        eng_w = eng_w.replace(lit, self.literal_letters[lit])
      englified_words.append(eng_w)
    return englified_words


  def separateEngGrWords(self, words, grammar, sentences):

    english_words = []
    english_grammar = []
    english_sentences = []
    greek_words = []
    greek_grammar = []
    greek_sentences = []

    for word in words:
      if re.match('[a-zA-Z\-]', word):
        rapp_print( "English word: " + str(word) )
        english_words.append( word )
      else:
        rapp_print( "Greek word: " + str(word) )
        greek_words.append( word )

    for word in grammar:
      if re.match('[a-zA-Z\-]', word):
        rapp_print( "English grammar: " + str(word) )
        english_grammar.append( word )
      else:
        rapp_print( "Greek grammar: " + str(word) )
        greek_grammar.append( word )

    for word in sentences:
      if re.match('[a-zA-Z\-]', word):
        rapp_print( "English sentence: " + str(word) )
        english_sentences.append( word )
      else:
        rapp_print( "Greek sentence: " + str(word) )
        greek_sentences.append( word )

    return [ english_words, english_grammar, english_sentences, greek_words, \
    greek_grammar, greek_sentences ]


  # Returns [conf, englified, status]
  # - conf is the configuration
  # - englified is a dictionary of the englified words
  # - status is either error (string) or True (bool)
  def getLimitedVocebularyConfiguration(self, words, grammar, sentences):

    # Seperate English for Greek words
    [ english_words, english_grammar, english_sentences, \
      greek_words, greek_grammar, greek_sentences ] = \
      self.separateEngGrWords( words, grammar, sentences )

    # Get phonemes for Greek words and dictionary for Englified->Greek mapping
    [englified_phonems_dict, englified_to_greek_dict] = \
        self.transformWords( greek_words )

    # Append english words to Englified->Greek mapping dictionary
    for word in english_words:
      englified_to_greek_dict.update( {word: word} )

    # Get phonemes for English words
    english_phonem_dict = self._english_support.getWordPhonemes( english_words )

    # Englify Greek grammar and sentences
    englified_grammar = self.englify_words(greek_grammar)
    englified_sentences = self.englify_words(greek_sentences)


    # Join English and Greek processed files
    final_phoneme_dict = english_phonem_dict
    final_phoneme_dict.update(englified_phonems_dict)
    final_sentences = englified_sentences + english_sentences
    final_grammar = english_grammar + englified_grammar

    try:
        self.limited_sphinx_configuration = \
            self.vocabulary.createConfigurationFiles( \
              final_phoneme_dict, final_grammar, final_sentences
            )
    except RappError as e:
        raise RappError(e.value)

    return [self.limited_sphinx_configuration, englified_to_greek_dict]

  def getGenericConfiguration(self):
    return self.generic_sphinx_configuration
