"""BombMod."""

# ba_meta require api 7

from __future__ import annotations
from typing import TYPE_CHECKING

import ba,_ba,random,time,weakref,json

from bastd.ui.radiogroup import make_radio_group
from bastd.ui.colorpicker import ColorPicker
from bastd.ui.play import PlayWindow
from bastd.actor.bomb import Bomb
from bastd.ui.popup import PopupWindow
from bastd.ui.tabs import TabRow

if TYPE_CHECKING: pass

config = ba.app.config

if config.get("Bomb Color") is None: config["Bomb Color"] = (1,0,0)
if config.get("Ice Color") is None: config["Ice Color"] = (1,0.5,0)
if config.get("Mine Color") is None: config["Mine Color"] = (1,1,0)
if config.get("Sticky Color") is None: config["Sticky Color"] = (0,1,0)
if config.get("Impact Color") is None: config["Impact Color"] = (0,1,1)
if config.get("TNT Color") is None: config["TNT Color"] = (0,0,1)
    
if config.get("Tab") is None: config["Tab"] = 0
if config.get("Shield") is None: config["Shield"] = True
if config.get("Bomb Scale") is None: config["Bomb Scale"] = 1
if config.get("Shield Scale") is None: config["Shield Scale"] = 0.75
if config.get("TNT Scale") is None: config["TNT Scale"] = 1
if config.get("Destello") is None: config["Destello"] = 1
    
if config.get("Normal Bomb") is None: config["Normal Bomb"] = True
if config.get("Ice Bomb") is None: config["Ice Bomb"] = False
if config.get("Mine Bomb") is None: config["Mine Bomb"] = False
if config.get("Sticky Bomb") is None: config["Sticky Bomb"] = False
if config.get("TNT Bomb") is None: config["TNT Bomb"] = True
if config.get("Impact Bomb") is None: config["Impact Bomb"] = False

if config.get("Fire Effect") is None: config["Fire Effect"] = 'Auto'
if config.get("Multicolors") is None: config["Multicolors"] = False

ba.app.config.apply_and_commit()

def translator(text):
    language = _ba.app.lang.language
    palabras = {"bombas": {"Spanish": 'Selecciona las bombas',"English": 'Select the bombs',"Portuguese": 'Selecione as bombas'},
    "shield": {"Spanish": 'Bombas con escudo',"English": 'Shield Bombs',"Portuguese": 'Bombas com escudo'},
    "size bombs": {"Spanish": 'Tamaño de bomba',"English": 'Bomb size',"Portuguese": 'Tamanho da bomba'},
    "normal bomb": {"Spanish": 'Bomba por defecto',"English": 'Default Bomb',"Portuguese": 'Bomba padrão'},
    "TNT": {"Spanish": 'Bomba TNT',"English": 'TNT Bomb',"Portuguese": 'Bomba TNT'},
    "shield": {"Spanish": 'Añadir escudo',"English": 'Add shield',"Portuguese": 'Adicionar escudo'},
    "color info": {"Spanish": 'Colores',"English": 'Colors',"Portuguese": 'Cores'},
    "settings": {"Spanish": 'Ajustes',"English": 'Settings',"Portuguese": 'configurações'},
    "shield size": {"Spanish": 'Tamaño del escudo',"English": 'Shield size',"Portuguese": 'Tamanho do escudo'},
    "TNT size": {"Spanish": 'Tamaño del TNT',"English": 'TNT size',"Portuguese": 'Tamanho do TNT'},
    "destello": {"Spanish": 'Destello',"English": 'Glow scale',"Portuguese": 'Escala de brilho'},
    "switch": {"Spanish": 'Interruptores',"English": 'Switches',"Portuguese": 'Switches'},
    "color select": {"Spanish": 'Selección de colores',"English": 'Color selection',"Portuguese": 'Seleção de cor'},
    "size info": {"Spanish": 'Ajustar tamaños',"English": 'Adjust sizes',"Portuguese": 'Ajustar tamanhos'},
    "fire info": {"Spanish": 'Bombas con fuego',"English": 'Fire bombs',"Portuguese": 'Bombas com fogo'},
    "activate": {"Spanish": 'Habilitar',"English": 'Enable',"Portuguese": 'Ativar'},
    "deactivate": {"Spanish": 'Inhabilitar',"English": 'Disable',"Portuguese": 'Desativar'},
    "multicolor": {"Spanish": 'Color cambiante',"English": 'Changing color',"Portuguese": 'Mudando de cor'}}
    idiomas = ["Spanish","English","Portuguese"]
    if language not in idiomas: language = "English"
    return palabras[text][language]

def getcolor(tag):
    acua = tag
    d = config['Destello']
    c = config['Bomb Color']
    c2 = config['Ice Color']
    c3 = config['Mine Color']
    c4 = config['Sticky Color']
    c5 = config['Impact Color']
    c6 = config['TNT Color']
    if acua == 1: s = (c[0]*d,c[1]*d,c[2]*d)
    elif acua == 2: s = (c2[0]*d,c2[1]*d,c2[2]*d)
    elif acua == 3: s = (c3[0]*d,c3[1]*d,c3[2]*d)
    elif acua == 4: s = (c4[0]*d,c4[1]*d,c4[2]*d)
    elif acua == 5: s = (c5[0]*d,c5[1]*d,c5[2]*d)
    else: s = (c6[0]*d,c6[1]*d,c6[2]*d)
    return s

def bomb_menu(self):
    rm = random.choice([(1,0,0),(1,1,0),(0,1,0),(0,0,1)])
    ba.buttonwidget(edit=self.button,color=rm)
    ba.containerwidget(edit=self._root_widget,transition='out_left')
    BombMenu()

# ba_meta export plugin
class BombMod(ba.Plugin):
    PlayWindow._old_init = PlayWindow.__init__
    def new_init(self,transition: str = 'in_right',origin_widget: ba.Widget = None):
        self._old_init(transition,origin_widget)
        
        x_offs = 100*6.4
        height = 550
        
        self.button = ba.buttonwidget(parent=self._root_widget,
                              position=(55 + x_offs, height - 155),
                              size=(60,60),scale=1.5,button_type='square',
                              texture=ba.gettexture('graphicsIcon'),
                              label='',color=(1,1,1),autoselect=True,
                              on_activate_call=ba.Call(bomb_menu,self))
    PlayWindow.__init__ = new_init
    
    Bomb._old_init = Bomb.__init__
    def new_init(self,position: Sequence[float] = (0.0, 1.0, 0.0),velocity: Sequence[float] = (0.0, 0.0, 0.0),bomb_type: str = 'normal',blast_radius: float = 2.0,bomb_scale: float = 1.0,source_player: ba.Player = None,owner: ba.Node = None):
        self._old_init(position,velocity,bomb_type,blast_radius,bomb_scale,source_player,owner)
        
        mscale = 1

        if ba.app.config['Normal Bomb']:
            if self.bomb_type == 'normal':
                mscale = config['Bomb Scale']
                if ba.app.config['Shield']:
                    self.shield = ba.newnode('shield',owner=self.node,attrs={'color': getcolor(1),'radius': config['Shield Scale']})
                    self.node.connectattr('position', self.shield, 'position')
        if ba.app.config['Ice Bomb']:
            if self.bomb_type == 'ice':
                mscale = config['Bomb Scale']
                if ba.app.config['Shield']:
                    self.shield = ba.newnode('shield',owner=self.node,attrs={'color': getcolor(2),'radius': config['Shield Scale']})
                    self.node.connectattr('position', self.shield, 'position')
        if ba.app.config['Sticky Bomb']:
            if self.bomb_type == 'sticky':
                mscale = config['Bomb Scale']
                if ba.app.config['Shield']:
                    self.shield = ba.newnode('shield',owner=self.node,attrs={'color': getcolor(4),'radius': config['Shield Scale']})
                    self.node.connectattr('position', self.shield, 'position')
        if ba.app.config['Mine Bomb']:
            if self.bomb_type == 'land_mine':
                mscale = config['Bomb Scale']
                if ba.app.config['Shield']:
                    self.shield = ba.newnode('shield',owner=self.node,attrs={'color': getcolor(3),'radius': config['Shield Scale']*1.2})
                    self.node.connectattr('position', self.shield, 'position')
        if ba.app.config['TNT Bomb']:
            if self.bomb_type == 'tnt':
                mscale = config['TNT Scale']
                if ba.app.config['Shield']:
                    self.shield = ba.newnode('shield',owner=self.node,attrs={'color': getcolor(6),'radius': config['Shield Scale']*1.5})
                    self.node.connectattr('position', self.shield, 'position')
        if ba.app.config['Impact Bomb']:
            if self.bomb_type == 'impact':
                mscale = config['Bomb Scale']
                if ba.app.config['Shield']:
                    self.shield = ba.newnode('shield',owner=self.node,attrs={'color': getcolor(5),'radius': config['Shield Scale']})
                    self.node.connectattr('position', self.shield, 'position')
                    
        if config['Fire Effect'] == 'Fire':
            def fire_effect():
                ba.emitfx(position=self.node.position,
                scale=1.3,count=50,spread=0.3,
                chunk_type='sweat')
            self._fire_time = ba.Timer(0.01,ba.Call(fire_effect),repeat=True) 
             
        if config['Multicolors']:
            def set_color(color):
                self._multicolors = color
                if self._multicolors == 1: f = getcolor(1)
                elif self._multicolors == 2: f = getcolor(2)
                elif self._multicolors == 3: f = getcolor(3)
                elif self._multicolors == 4: f = getcolor(4)
                elif self._multicolors == 5: f = getcolor(5)
                else: f = getcolor(6)
                self.shield.color = f
            def color_rainbow():
                ba.timer(1,ba.Call(set_color,1),timeformat=ba.TimeFormat.MILLISECONDS)
                ba.timer(400,ba.Call(set_color,2),timeformat=ba.TimeFormat.MILLISECONDS)
                ba.timer(800,ba.Call(set_color,3),timeformat=ba.TimeFormat.MILLISECONDS)
                ba.timer(1200,ba.Call(set_color,4),timeformat=ba.TimeFormat.MILLISECONDS)
                ba.timer(1600,ba.Call(set_color,5),timeformat=ba.TimeFormat.MILLISECONDS)
                ba.timer(2000,ba.Call(set_color,6),timeformat=ba.TimeFormat.MILLISECONDS)
            color_rainbow()
            self._rainbow_time = ba.Timer(2.4,ba.Call(color_rainbow),repeat=True)
        ba.animate(self.node, 'model_scale', {0: 0,0.2: 1.3 * mscale,0.26: mscale})
    Bomb.__init__ = new_init
    
    def new_handle_die(self):
        if self.node:
            self.node.delete()
            self._rainbow_time = None
            self._fire_time = None
    Bomb._handle_die = new_handle_die
    
class BombMenu(PopupWindow):
    def __init__(self, transition= 'in_right'):
        self._width = width = 600
        self._height = height = 420
        self._sub_height = 200
        self._scroll_width = self._width*0.90
        self._scroll_height = self._height - 180
        self._sub_width = self._scroll_width*0.95;

        self._current_tab = config['Tab']
        self._bomb_scale = config['Bomb Scale']
        self._shield_scale = config['Shield Scale']
        self._TNT_scale = config['TNT Scale']
        self._destello = config['Destello']

        app = ba.app.ui
        uiscale = app.uiscale
                                       
        self._root_widget = ba.containerwidget(size=(width,height),transition=transition,
                           scale=1.5,color=(0.24,0.24,0.24),
                           stack_offset=(0,-30) if uiscale is ba.UIScale.SMALL else  (0,0))
        
        self._backButton = b = ba.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(20,self._height-50),size=(130,60),
                                               scale=0.8,text_scale=1.2,label=ba.Lstr(resource='backText'),
                                               button_type='back',on_activate_call=ba.Call(self._back))
        ba.buttonwidget(edit=self._backButton, button_type='backSmall',size=(60, 60),label=ba.charstr(ba.SpecialChar.BACK))

        ba.containerwidget(edit=self._root_widget,cancel_button=b)
        self.titletext = ba.textwidget(parent=self._root_widget,position=(0, height-20),size=(width,50),
                          h_align="center",color=(1,1,1), v_align="center",maxwidth=width*1.3)
												
        self._scrollwidget = ba.scrollwidget(parent=self._root_widget,
                                             position=(self._width*0.08,51*1.1),
                                             size=(self._sub_width,self._scroll_height +60*1.2),selection_loops_to_parent=True)

        #### ->
        tabdefs = [[0,translator('bombas')],
                    [1,translator('shield')],
                    [2,translator('settings')]]

        self._tab_row = TabRow(self._root_widget,tabdefs,
                               pos=(self._width*0.37 -80*1.8, 87+self._scroll_height+36),
                               size=(self._scroll_width*0.85,0),
                               on_select_call=self._set_tab)
                    
        self._tab_container = None
        self._set_tab(self._current_tab)
        
    def _set_tab(self, tab):
        self._current_tab = tab
        ba.app.config['Tab'] = tab
        ba.app.config.apply_and_commit()
        
        if self._tab_container is not None and self._tab_container.exists():
            self._tab_container.delete()
        self._tab_data = {}
        
        self._tab_row.update_appearance(tab)
        
        if tab == 0:
            sub_height = 360
            v = sub_height - 55
            c_width = self._scroll_width
            c_height = min(self._scroll_height, 200*1.0+100)
            ba.textwidget(edit=self.titletext, text=translator('bombas'))
            
            self._tab_container = c = ba.containerwidget(parent=self._scrollwidget,
                            size=(self._sub_width,sub_height),
                            background=False,selection_loops_to_parent=True)
        
            mv = 60*1.5
            v = sub_height + 55
            n = 30
            self.check = ba.checkboxwidget(parent=c,position=(n,v-mv),value=ba.app.config['Normal Bomb'],color=config['Bomb Color'],
                    on_value_change_call=ba.Call(self._switches,'Normal Bomb'),maxwidth=self._scroll_width*0.9,
                    text=translator('normal bomb')+"(1)",autoselect=True, textcolor=config['Bomb Color'])
    
            t = -60*1 - mv
            self.check = ba.checkboxwidget(parent=c,position=(n,v+t),value=ba.app.config['Ice Bomb'],color=config['Ice Color'],
                    on_value_change_call=ba.Call(self._switches,'Ice Bomb'),maxwidth=self._scroll_width*0.9,textcolor=config['Ice Color'],
                    text=ba.Lstr(resource='helpWindow.'+'powerupIceBombsNameText').evaluate()+"(2)",autoselect=True)
                    
            t = -60*2 - mv
            self.check = ba.checkboxwidget(parent=c,position=(n,v+t),value=ba.app.config['Mine Bomb'],color=config['Mine Color'],
                    on_value_change_call=ba.Call(self._switches,'Mine Bomb'),maxwidth=self._scroll_width*0.9,textcolor=config['Mine Color'],
                    text=ba.Lstr(resource='helpWindow.'+'powerupLandMinesNameText').evaluate()+"(3)",autoselect=True)
    
            t = -60*3 - mv
            self.check = ba.checkboxwidget(parent=c,position=(n,v+t),value=ba.app.config['Sticky Bomb'],color=config['Sticky Color'],
                    on_value_change_call=ba.Call(self._switches,'Sticky Bomb'),maxwidth=self._scroll_width*0.9,textcolor=config['Sticky Color'],
                    text=ba.Lstr(resource='helpWindow.'+'powerupStickyBombsNameText').evaluate()+"(4)",autoselect=True)
                    
            t = -60*4 - mv
            self.check = ba.checkboxwidget(parent=c,position=(n,v+t),value=ba.app.config['Impact Bomb'],color=config['Impact Color'],
                    on_value_change_call=ba.Call(self._switches,'Impact Bomb'),maxwidth=self._scroll_width*0.9,textcolor=config['Impact Color'],
                    text=ba.Lstr(resource='helpWindow.'+'powerupImpactBombsNameText').evaluate()+"(5)",autoselect=True)
                    
            t = -60*5 - mv
            self.check = ba.checkboxwidget(parent=c,position=(n,v+t),value=ba.app.config['TNT Bomb'],color=config['TNT Color'],
                    on_value_change_call=ba.Call(self._switches,'TNT Bomb'),maxwidth=self._scroll_width*0.9,textcolor=config['TNT Color'],
                    text=translator('TNT')+"(6)",autoselect=True)
        elif tab == 1:
            sub_height = 540
            width = 700
            v = sub_height - 55
            sc = 1.3
            c_width = self._scroll_width
            c_height = min(self._scroll_height, 200*1+100)
            ba.textwidget(edit=self.titletext, text=translator('shield'))

            self._tab_container = c = ba.containerwidget(parent=self._scrollwidget,
                            size=(self._sub_width,sub_height),
                            background=False,selection_loops_to_parent=True)

            i = 60*2.8
            n = 30
            s = 60*2
            v = sub_height - 55*3
            
            nv = 90
            self._text = ba.textwidget(parent=c,position=(i - 60*5 +30,v +nv),size=(width,50),scale=sc,
                          text=translator('switch'),  h_align="center",color=(1,1,1), v_align="center",maxwidth=width*0.6)
            
            i = 60*4
            nv = 40
            
            cl = (0.8, 0.8, 0.8)
            self.check = ba.checkboxwidget(parent=c,position=(n+i-s,v+nv),value=ba.app.config['Shield'],color=cl,
                    on_value_change_call=ba.Call(self._switches,'Shield'),maxwidth=self._scroll_width*0.9,textcolor=cl,
                    text=translator('shield'),autoselect=True)
                    
            gi = 60
            self.check = ba.checkboxwidget(parent=c,position=(n+i-s,v-gi+nv),value=ba.app.config['Multicolors'],color=cl,
                    on_value_change_call=ba.Call(self._multicolors),maxwidth=self._scroll_width*0.9,textcolor=cl,
                    text=translator('multicolor'),autoselect=True)

            i = 20*1
            v = sub_height - 55*4.5
            o = 150*2
            j = 1
            self._preview = ba.buttonwidget(parent=c,autoselect=True,
                position=(n+o+i+60,v-60*0.7+j-90),size=(60,60),texture=ba.gettexture('ouyaOButton'),
                scale=1.1,text_scale=1.2,label='',color=(0.7,0.7,0.7),on_activate_call=ba.Call(self._preview_button),
                button_type='square')
            if config['Multicolors']:
                self._update_preview()
                self._preview_color = ba.Timer(2.4,ba.Call(self._update_preview),repeat=True)
            else: self._preview_color = None
    
            o = -150
            self._text = ba.textwidget(parent=c,position=(o+i+30,v-50*0.7+j-25),size=(width,50),scale=sc,
                          text=translator('color select'),  h_align="center",color=(1,1,1), v_align="center",maxwidth=width*0.6)
    
            i = 60*1.5
            v = sub_height - 55*5
            self._colorpicker_button = ba.buttonwidget(parent=c,autoselect=True,
                position=(n+i,v-60*2),size=(60,60),
                scale=1.1,text_scale=1.2,label="1",color=ba.app.config['Bomb Color'],
                button_type='square',on_activate_call=ba.Call(self._make_picker,'Normal'))
            self._colorpicker_button2 = ba.buttonwidget(parent=c,autoselect=True,
                position=(n+n*3+i,v-60*2),size=(60,60),
                scale=1.1,text_scale=1.2,label="2",color=ba.app.config['Ice Color'],
                button_type='square',on_activate_call=ba.Call(self._make_picker,'Ice'))
            self._colorpicker_button3 = ba.buttonwidget(parent=c,autoselect=True,
                position=(n+n*6+i,v-60*2),size=(60,60),
                scale=1.1,text_scale=1.2,label="3",color=ba.app.config['Mine Color'],
                button_type='square',on_activate_call=ba.Call(self._make_picker,'Mine'))

            self._colorpicker_button4 = ba.buttonwidget(parent=c,autoselect=True,
                position=(n+i,v-60*4),size=(60,60),
                scale=1.1,text_scale=1.2,label="4",color=ba.app.config['Sticky Color'],
                button_type='square',on_activate_call=ba.Call(self._make_picker,'Sticky'))
            self._colorpicker_button5 = ba.buttonwidget(parent=c,autoselect=True,
                position=(n+n*3+i,v-60*4),size=(60,60),
                scale=1.1,text_scale=1.2,label="5",color=ba.app.config['Impact Color'],
                button_type='square',on_activate_call=ba.Call(self._make_picker,'Impact'))
            self._colorpicker_button6 = ba.buttonwidget(parent=c,autoselect=True,
                position=(n+n*6+i,v-60*4),size=(60,60),
                scale=1.1,text_scale=1.2,label="6",color=ba.app.config['TNT Color'],
                button_type='square',on_activate_call=ba.Call(self._make_picker,'TNT'))
        else:
            sub_height = 450
            v = sub_height - 55
            width = 700
            c_width = self._scroll_width
            c_height = min(self._scroll_height, 200*1.0+100)
            ba.textwidget(edit=self.titletext, text=translator('settings'))

            self._tab_container = c = ba.containerwidget(parent=self._scrollwidget,
                            size=(self._sub_width,sub_height),
                            background=False,selection_loops_to_parent=True)
                    
            t = ba.textwidget(parent=c,position=(60*5-40 -360,v-60*2.8),size=(width,50),scale=1.2,
                          text=translator('size info'),  h_align="center",color=(1,1,1), v_align="center",maxwidth=width*0.6)
                    
            #BOMBA
            v = sub_height - 70*3.5
            g = 55
            i = 50
            f = 60*1
            sc = ba.buttonwidget(parent=c,position=(20 + g - i,v - f),size=(40,40),label="-",
                            autoselect=True,on_activate_call=ba.Call(self.decrement),repeat=True,enable_sound=True,button_type='square')
                            
            sc2 = ba.buttonwidget(parent=c,position=(20*8 + g - i,v - f),size=(40,40),label="+",
                            autoselect=True,on_activate_call=ba.Call(self.increment),repeat=True,enable_sound=True,button_type='square')

            q = 400
            self._scaletext = ba.textwidget(parent=c,position=(-q +20*8 + g - i,v - f),size=(width,50),
                          text=str(self._bomb_scale),  h_align="center",color=(2,1,1), v_align="center",maxwidth=width*0.6)
            m = 40
            t = ba.textwidget(parent=c,position=(-q +20*8 + g - i,v - f + m),size=(width,50),
                          text=translator('size bombs'),  h_align="center",color=(2,1,1), v_align="center",maxwidth=width*0.6)
                    
            #ESCUDO
            f = 60*3
            sc = ba.buttonwidget(parent=c,position=(20 + g - i,v - f),size=(40,40),label="-",
                            autoselect=True,on_activate_call=ba.Call(self.decrement2),repeat=True,enable_sound=True,button_type='square')
                            
            sc2 = ba.buttonwidget(parent=c,position=(20*8 + g - i,v - f),size=(40,40),label="+",
                            autoselect=True,on_activate_call=ba.Call(self.increment2),repeat=True,enable_sound=True,button_type='square')

            self._scaletext_shield = ba.textwidget(parent=c,position=(-q +20*8 + g - i,v - f),size=(width,50),
                          text=str(self._shield_scale),  h_align="center",color=(2,2,1), v_align="center",maxwidth=width*0.6)
                         
            t = ba.textwidget(parent=c,position=(-q +20*8 + g - i,v - f + m),size=(width,50),
                          text=translator('shield size'),  h_align="center",color=(2,2,1), v_align="center",maxwidth=width*0.6)
 
            #TNT
            f = 60*1
            i = 60*3.6
            sc = ba.buttonwidget(parent=c,position=(20 + g + i,v - f),size=(40,40),label="-",
                            autoselect=True,on_activate_call=ba.Call(self.decrement3),repeat=True,enable_sound=True,button_type='square')
                            
            sc2 = ba.buttonwidget(parent=c,position=(20*8 + g + i,v - f),size=(40,40),label="+",
                            autoselect=True,on_activate_call=ba.Call(self.increment3),repeat=True,enable_sound=True,button_type='square')

            self._scaletext_TNT = ba.textwidget(parent=c,position=(-q +20*8 + g + i,v - f),size=(width,50),
                          text=str(self._TNT_scale),  h_align="center",color=(1,2,1), v_align="center",maxwidth=width*0.6)
                       
            t = ba.textwidget(parent=c,position=(-q +20*8 + g + i,v - f + m),size=(width,50),
                          text=translator('TNT size'),  h_align="center",color=(1,2,1), v_align="center",maxwidth=width*0.6)
   
            #DESTELLO
            f = 60*3
            sc = ba.buttonwidget(parent=c,position=(20 + g + i,v - f),size=(40,40),label="-",
                            autoselect=True,on_activate_call=ba.Call(self.decrement4),repeat=True,enable_sound=True,button_type='square')
                            
            sc2 = ba.buttonwidget(parent=c,position=(20*8 + g + i,v - f),size=(40,40),label="+",
                            autoselect=True,on_activate_call=ba.Call(self.increment4),repeat=True,enable_sound=True,button_type='square')

            self._destello_txt = ba.textwidget(parent=c,position=(-q +20*8 + g + i,v - f),size=(width,50),
                          text=str(self._destello),  h_align="center",color=(1,1,2), v_align="center",maxwidth=width*0.6)
                    
            t = ba.textwidget(parent=c,position=(-q +20*8 + g + i,v - f + m),size=(width,50),
                          text=translator('destello'),  h_align="center",color=(1,1,2), v_align="center",maxwidth=width*0.6)
                    
            #SWITCH
            e = 20*2.5
            u = 40*0.8
            sl = 0.9
            cl = (0.8, 0.8, 0.8)
            v = sub_height - 70*2.2
            
            fire_effect = config.get('Fire Effect')

            sw1 = ba.checkboxwidget(parent=c,position=(60*2.5-e,v+30*3-u),
                    maxwidth=self._scroll_width*0.9,scale=sl,textcolor=cl,color=cl,
                    text=translator('activate'),autoselect=True)          
            sw2 = ba.checkboxwidget(parent=c,position=(60*5-e,v+30*3-u),
                    maxwidth=self._scroll_width*0.9,scale=sl,textcolor=cl,color=cl,
                    text=translator('deactivate'),autoselect=True)
            make_radio_group((sw1, sw2), ('Fire', 'Auto'), fire_effect, self._actions_changed)        
                    
            t = ba.textwidget(parent=c,position=(60*5-40 -360,v+30*3),size=(width,50),scale=1.2,
                          text=translator('fire info'),  h_align="center",color=(1,1,1), v_align="center",maxwidth=width*0.6)
                    
    def _make_picker(self,tag):
        if tag == 'Normal': initial_color = ba.app.config['Bomb Color']
        elif tag == 'Ice': initial_color = ba.app.config['Ice Color']
        elif tag == 'Mine': initial_color = ba.app.config['Mine Color']
        elif tag == 'Sticky': initial_color = ba.app.config['Sticky Color']
        elif tag == 'Impact': initial_color = ba.app.config['Impact Color']
        elif tag == 'TNT': initial_color = ba.app.config['TNT Color']
        ColorPicker(parent=self._root_widget,position=(0,0),
        initial_color=initial_color,delegate=self,tag=tag)
    
    def color_picker_closing(self, picker):
        pass

    def color_picker_selected_color(self, picker, color):
        tag = picker.get_tag()
        if tag == 'Normal':
            ba.app.config['Bomb Color'] = color
            if self._colorpicker_button:
                ba.buttonwidget(edit=self._colorpicker_button, color=color)
        elif tag == 'Ice':
            ba.app.config['Ice Color'] = color
            if self._colorpicker_button2:
                ba.buttonwidget(edit=self._colorpicker_button2, color=color)
        elif tag == 'Mine':
            ba.app.config['Mine Color'] = color
            if self._colorpicker_button3:
                ba.buttonwidget(edit=self._colorpicker_button3, color=color)
        elif tag == 'Sticky':
            ba.app.config['Sticky Color'] = color
            if self._colorpicker_button4:
                ba.buttonwidget(edit=self._colorpicker_button4, color=color)
        elif tag == 'Impact':
            ba.app.config['Impact Color'] = color
            if self._colorpicker_button5:
                ba.buttonwidget(edit=self._colorpicker_button5, color=color)            
        elif tag == 'TNT':
            ba.app.config['TNT Color'] = color
            if self._colorpicker_button6:
                ba.buttonwidget(edit=self._colorpicker_button6, color=color)             
                
    def decrement(self):
        self._bomb_scale = max(0.5,self._bomb_scale - 0.25)
        ba.textwidget(edit=self._scaletext,text=str(self._bomb_scale))
        config['Bomb Scale'] =  self._bomb_scale
        ba.app.config.apply_and_commit()
		
    def increment(self):
        self._bomb_scale = min(3.0,self._bomb_scale + 0.25)
        ba.textwidget(edit=self._scaletext,text=str(self._bomb_scale))
        config['Bomb Scale'] =  self._bomb_scale
        ba.app.config.apply_and_commit()
        
    def decrement2(self):
        self._shield_scale = max(0.5,self._shield_scale - 0.25)
        ba.textwidget(edit=self._scaletext_shield,text=str(self._shield_scale))
        config['Shield Scale'] =  self._shield_scale
        ba.app.config.apply_and_commit()
		
    def increment2(self):
        self._shield_scale = min(4.0,self._shield_scale + 0.25)
        ba.textwidget(edit=self._scaletext_shield,text=str(self._shield_scale))
        config['Shield Scale'] =  self._shield_scale
        ba.app.config.apply_and_commit()
        
    def decrement3(self):
        self._TNT_scale = max(0.5,self._TNT_scale - 0.25)
        ba.textwidget(edit=self._scaletext_TNT,text=str(self._TNT_scale))
        config['TNT Scale'] =  self._TNT_scale
        ba.app.config.apply_and_commit()
		
    def increment3(self):
        self._TNT_scale = min(1.5,self._TNT_scale + 0.25)
        ba.textwidget(edit=self._scaletext_TNT,text=str(self._TNT_scale))
        config['TNT Scale'] =  self._TNT_scale
        ba.app.config.apply_and_commit()
        
    def decrement4(self):
        self._destello = max(1,self._destello - 1)
        ba.textwidget(edit=self._destello_txt,text=str(self._destello))
        config['Destello'] =  self._destello
        ba.app.config.apply_and_commit()
		
    def increment4(self):
        self._destello = min(5,self._destello + 1)
        ba.textwidget(edit=self._destello_txt,text=str(self._destello))
        config['Destello'] =  self._destello
        ba.app.config.apply_and_commit()
    
    def _switches(self,tag,m):
        ba.app.config[tag] = False if m==0 else True
        ba.app.config.apply_and_commit()
        
    def _multicolors(self,m):
        ba.app.config['Multicolors'] = False if m==0 else True
        ba.app.config.apply_and_commit()
        if config['Multicolors']: self._preview_color = ba.Timer(2.4,ba.Call(self._update_preview),repeat=True)
        else: self._preview_color = None    
            
    def _actions_changed(self, tag):
        ba.app.config['Fire Effect'] = tag
        ba.app.config.apply_and_commit()
            
    def _update_preview(self):
        ba.timer(1,ba.Call(self.preview_color,1),timeformat=ba.TimeFormat.MILLISECONDS)
        ba.timer(400,ba.Call(self.preview_color,2),timeformat=ba.TimeFormat.MILLISECONDS)
        ba.timer(800,ba.Call(self.preview_color,3),timeformat=ba.TimeFormat.MILLISECONDS)
        ba.timer(1200,ba.Call(self.preview_color,4),timeformat=ba.TimeFormat.MILLISECONDS)
        ba.timer(1600,ba.Call(self.preview_color,5),timeformat=ba.TimeFormat.MILLISECONDS)
        ba.timer(2000,ba.Call(self.preview_color,6),timeformat=ba.TimeFormat.MILLISECONDS)

    def _preview_button(self):
        rm = (1,1,1)
        c = config['Bomb Color']
        c2 = config['Ice Color']
        c3 = config['Mine Color']
        c4 = config['Sticky Color']
        c5 = config['Impact Color']
        c6 = config['TNT Color']
        ba.screenmessage("1 = "+ str(c)+"\n2 = "+str(c2)+"\n3 = "+str(c3)+"\n4 = "+str(c4)+"\n5 = "+str(c5)+"\n6 = "+str(c6),color=rm)
        
    def preview_color(self,tag):
        prev = tag
        if prev == 1: s = getcolor (1)
        elif prev == 2: s = getcolor (2)
        elif prev == 3: s = getcolor (3)
        elif prev == 4: s = getcolor (4)
        elif prev == 5: s = getcolor (5)
        else: s = getcolor(6)
        ba.buttonwidget(edit=self._preview,color=s)
 
    def _back(self):
        self._preview_color = None
        ba.containerwidget(edit=self._root_widget,transition='out_right')
        ba.app.main_menu_window = PlayWindow(transition='in_left').get_root_widget()