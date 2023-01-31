"""
OBC master, EPS slave
I2C protocol : SDA, SCL
"""

"""Initalising variables"""
position=0
position_out=0
WORD_FROM_OBC=0
WORD_TO_OBC=0

"""STM32 INPUT FROM OBC, the instructions we're receiving from the OBC and the specified frame constants"""
STARTING_IN_4BIT  = 9 #constant
#PAYLOAD_IN_4BIT  
#UHF_IN_3BIT      
#XBAND_IN_4BIT
PAYLOAD_ON  = 4
PAYLOAD_OFF = 6
UHF_ON      = 1
UHF_OFF     = 3
XBAND_ON    = 7
XBAND_OFF   = 12
ENDING_IN_2BIT    = 3 #constant

"""STM32 OUTPUT TO OBC, the telemetry we're sending to the OBC and the specified frame constants"""
STARTING_OUT_4BIT = 9 #constant
PAYLOAD_OUT_2BIT  = 0 # this is just initialising but the valid values are 1 (ON) or 3 (OFF)
UHF_OUT_2BIT      = 0 # this is just initialising but the valid values are 1 (ON) or 3 (OFF)
XBAND_OUT_2BIT    = 0 # this is just initialising but the valid values are 1 (ON) or 3 (OFF)
CHARGE_OUT_7BIT   = 0 # this is just initialising but the valid values are 0 to 100
TEMP_OUT_8BIT     = 0 # this is just initialising but the valid values are -128 to 127
ENDING_OUT_2BIT   = 3 #constant

payload_STATE  = #read from pin powering the payload mosfet
uhf_STATE      = #read from pin powering the uhf mosfet
xband_STATE    = #read from pin powering the xband mosfet
battery_CHARGE = #read from the battery balancing circuit
battery_TEMPERATURE= #read from battery board thermometer circuit

def read_PIN_SCL_FROM_OBC():
    return 0
def read_PIN_SDA_FROM_OBC():
    return 0
def set_PIN_SDA_TO_OBC(value):
    if (value):
    if (not value):
def payload_ON():
    PAYLOAD_OUT_2BIT=1
    #activate payload supply mosfet
def payload_OFF():
    PAYLOAD_OUT_2BIT=3
    #deactivate payload supply mosfet
def uhf_ON():
    UHF_OUT_2BIT=1
    #activate uhf supply  mosfet
def uhf_OFF():
    UHF_OUT_2BIT=3
    #deactivate uhf supply mosfet
def xband_ON():
    XBAND_OUT_2BIT=1
    #activate xband supply mosfet
def xband_OFF():
    XBAND_OUT_2BIT=3
    #deactivate xband supply mosfet
def RELEASE_ONE():
    #release switch 1, return True  means it's activated
def RELEASE_TWO():
    #release switch 2, return True  means it's activated
def RELEASE_THREE():
    #release switch 3, return True  means it's activated
def RELEASE_FOUR():
    #release switch 4, return True  means it's activated
def deploy_PANELS():
    #activate motors to deploy panels
    
while(True):
    if (position    ==48) : position     = 0 #0 to 47, bit position counter reset
    if (position_out==48) : position_out = 0 #0 to 47, bit position counter reset
    
    ##OBC TO EPS##
    if (read_PIN_SCL1_FROM_OBC()) :# if SCL is high then data is coming in from OBC
        sda = read_PIN1_SDA_FROM_OBC()
        if(  sda   ) : WORD_FROM_OBC = (WORD_FROM_OBC | (  1<<(47-position) )) #store 1 bit at position
        if(not sda ) : WORD_FROM_OBC = (WORD_FROM_OBC & (~(1<<(47-position)))) #store 0 bit at position
        if( ((WORD_FROM_OBC>>32) == STARTING_IN_8BIT) and ((WORD_FROM_OBC&255) == ENDING_IN_8BIT) ):#start and end
            if( ((WORD_FROM_OBC>>24)&255 ) == PAYLOAD_ON  ) : payload_ON()
            if( ((WORD_FROM_OBC>>24)&255 ) == PAYLOAD_OFF ) : payload_OFF()
            if( ((WORD_FROM_OBC>>16)&255 ) == UHF_ON      ) : uhf_ON()
            if( ((WORD_FROM_OBC>>16)&255 ) == UHF_OFF     ) : uhf_OFF()
            if( ((WORD_FROM_OBC>>8 )&255 ) == XBAND_ON    ) : xband_ON()
            if( ((WORD_FROM_OBC>>8 )&255 ) == XBAND_OFF   ) : xband_OFF()
        
    ##EPS TO OBC##
    if(read_PIN_SCL2_FROM_OBC()):
        if(postion==0):
        if( ((WORD_FROM_OBC>>7) == STARTING_IN_9BIT) and ((WORD_FROM_OBC&63) == ENDING_IN_6BIT) ):#start and end    
            if( (WORD_FROM_OBC>>7)== &7 == PAYLOAD_ON  ): payload_ON()
            if( ((WORD_FROM_OBC>>14)&7) == PAYLOAD_OFF ): payload_OFF()
            if( ((WORD_FROM_OBC>>10)&15 ) == UHF_ON    ): uhf_ON()
            if( ((WORD_FROM_OBC>>10)&15 ) == UHF_OFF   ): uhf_OFF()
            if( ((WORD_FROM_OBC>>6)&15) == XBAND_ON    ): xband_ON()
            if( ((WORD_FROM_OBC>>6)&15) == XBAND_OFF   ): xband_OFF()
            
    set_PIN_SDA_TO_OBC( WORD_TO_OBC & (1<<(25-position)) )
    if(RELEASE_ONE and RELEASE_TWO and RELEASE_THREE and RELEASE_FOUR): deploy_PANELS()
    WORD_TO_OBC =  ( 
                     (STARTING_OUT_8BIT<<48) | 
                         (payload_STATE<<46) |
                             (uhf_STATE<<44) |
                           (xband_STATE<<42) |
                             (panel_ONE<<37) |
                             (panel_TWO<<32) |
                           (panel_THREE<<27) |
                            (panel_FOUR<<22) |
                          (battery_VOLT<<17) |
                    (battery_TEMPERATURE<<8) |
                             ENDING_OUT_8BIT
                   )   
    while( read_PIN_SCL_FROM_OBC() ):#Pause        
    position     = position+1
    position_out = position_out+1


