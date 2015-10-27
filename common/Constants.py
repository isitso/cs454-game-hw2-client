# define Constants

class Constants:
    SERVER_IP = 'localhost'
    SERVER_PORT = 9252
    DEBUG = True
    MSG_NONE                            = 0

    C_AUTH                              = 101
    C_DISCONNECT                        = 102
    C_GO_TO_CHARACTER_SELECTION         = 103
    C_SELECT_CHARACTER                  = 104
    C_REGISTER                          = 105
    C_CREATE_CHARACTER                  = 106
    C_MOVE                              = 110
    C_CHAT                              = 111
    C_HEARTBEAT                         = 120
    
    S_AUTH                              = 201
    S_DISCONNECT                        = 202
    S_GO_TO_CHARACTER_SELECTION         = 203
    S_SELECT_CHARACTER                  = 204
    S_REGISTER                          = 205
    S_CREATE_CHARACTER                  = 206
    S_PLAYER_MOVE                       = 210
    S_PLAYER_LOGOUT                     = 212
    S_CHAT                              = 211
    S_SPAWN                             = 213

    GAMESTATE_NOT_LOGGED_IN             = 0
    GAMESTATE_LOGGED_IN                 = 1
    GAMESTATE_PLAYING                   = 2

    CHAR_RALPH                          = 1
    CHAR_VEHICLE                        = 2
    CHAR_PANDA                          = 3
