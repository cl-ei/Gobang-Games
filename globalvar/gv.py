"""
#此文件包含部分全局变量

#包括：
#    窗体分辨率数据
#    各元素相对位置
#    资源文件路径

"""

#windows size (width,height)
g_size_win = (800,600)
g_icon_fileloc = "./img/head.png"
g_wintitle  = "CL的五子棋"

g_size_btn = (133,75)
g_size_btn_gameback = (80,40)

g_pos_btn_start = (200,400)    
g_pos_btn_about = (400,400)
g_pos_btn_back = (g_size_win[0]//2.5,g_size_win[1]//1.2)
g_pos_btn_gameback = (20,500)
g_pos_btn_goback = (26,30)
g_pos_btn_goahead = (24,130)
g_screen  = None
g_clock   = None

g_home_img_fileloc = "./img/homepage.png"
g_home_img = None
g_surfaceback_img_fileloc = "./img/about_background.png"

g_btn_start_imgloc = ("img/btn_start_game.png",
                      "img/btn_start_game_focus.png",
                      "img/btn_start_game_down.png")

g_btn_about_imgloc = ("img/btn_about.png",
                      "img/btn_about_focus.png",
                      "img/btn_about_down.png")

g_btn_back_imgloc  = ("img/btn_back.png",
                      "img/btn_back_focus.png",
                      "img/btn_back_down.png")

g_btn_gameback_imgloc  = ("img/btn_back.png",
                          "img/btn_back_focus.png",
                          "img/btn_back_down.png")

g_btn_goback_imgloc  = ("img/btn_goback.png",
                        "img/btn_goback_focus.png",
                        "img/btn_goback_down.png")

g_btn_goahead_imgloc  = ("img/btn_goahead.png",
                        "img/btn_goahead_focus.png",
                        "img/btn_goahead_down.png")

#grid border
g_width_grid     = 30
g_pos_grid_start = (170,60)
g_size_grid      =  440

g_black  = (30,30,30)
g_white = (255,255,255)

g_font  = None

g_txt_w_thinking = None
g_txt_b_thinking = None

g_font_for_btn = "sourcefile/ncsj.ttf"

g_num_tab = []