from games.pingpong.ml.Moduls import CSV_Read_2P
import math
"""
The template of the script for the machine learning process in game pingpong
"""

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the MLPlay is used by
               which side.
        """
        self.ball_served = False
        self.side = "2P"

    def update(self, scene_info):
        # Make the caller to invoke reset() for the next round.
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        else: 
            #print(scene_info)
            BallCoordinate_Now = scene_info["ball"] #球當前位置
            ball_speed = scene_info["ball_speed"]   #球速
            PlatformX = scene_info["platform_2P"][0] + 20  #板子x位置_2P
            PlatformY = scene_info["platform_2P"][1] + 20  #板子y位置_2P
            PlatformX_2P = scene_info["platform_1P"][0] + 20 #板子x位置_1P
            PlatformY_2P = scene_info["platform_1P"][1] + 20 #板子y位置_1P
            Frame = scene_info["frame"] #偵數
            BallUpAndDown = ''
            aid = 0
            m = 1
            BallUpAndDown_NUM = 0
            if ball_speed[0] != 0:
                m = ball_speed[1] / ball_speed[0]
                aid = BallCoordinate_Now[0] + (math.ceil((80 - BallCoordinate_Now[1]) / ball_speed[1]) * ball_speed[0])  #math.ceil無條件進位，出現小數點會導致板子多跑x軸 y在80和420則停止，x會跑完該跑的

            if aid < 0:
                aid = -aid
            if aid > 195:
                aid = aid - 195
                aid = 195 - aid
            
            if ball_speed[1] < 0:    #0是x 1是y
                BallUpAndDown = 'up'
                BallUpAndDown_NUM = 0
            else:
                BallUpAndDown = 'down'
                BallUpAndDown_NUM = 1
                
            print(BallUpAndDown,BallCoordinate_Now,ball_speed,aid,Frame)
            CSV_Read_2P.doWrite(Frame, BallCoordinate_Now[0], BallCoordinate_Now[1], m, ball_speed[0], ball_speed[1], PlatformX, PlatformY, PlatformX_2P, PlatformY_2P, BallUpAndDown_NUM)

            if BallUpAndDown == 'up' and PlatformX > aid :
                return "MOVE_LEFT"
            if BallUpAndDown == 'up' and PlatformX < aid :
                return "MOVE_RIGHT"

            if BallUpAndDown == 'down' and PlatformX < 100:
                return "MOVE_RIGHT"

            if BallUpAndDown == 'down' and PlatformX > 100:
                return "MOVE_LEFT"

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False