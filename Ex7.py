import random
import arcade
import arcade.gui

MOVEMENT_SPEED = 5

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
COIN_COUNT = 40
MEDAL_COUNT = 10

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Collect Coins Example"


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        super().__init__(800, 600, "MessageBox", resizable=True)
        arcade.set_background_color(arcade.color.COOL_GREY)

        # Create and enable the UIManager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.message_box = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.medal_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.checkpoint = 0

        # Don't show the mouse cursor
        #self.set_mouse_visible(False)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.medal_list = arcade.SpriteList()
        # Score
        self.score = 0
        self.checkpoint = 0

        # Set up the player
        # Character image from kenney.nl
        img = "playerFace.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite("coinGold.png",SPRITE_SCALING_COIN)
            medal = arcade.Sprite("medal3.png", SPRITE_SCALING_COIN)
            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)
        
        # Create the medals
        for i in range(MEDAL_COUNT):
            # Create the coin instance
            # Coin image from kenney.nl
            #coin = arcade.Sprite("coinGold.png",SPRITE_SCALING_COIN)
            medal = arcade.Sprite("medal3.png", SPRITE_SCALING_COIN)
            # Position the coin
            
            medal.center_x = random.randrange(SCREEN_WIDTH)
            medal.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.medal_list.append(medal)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.coin_list.draw()
        self.medal_list.draw()
        self.player_list.draw()
        self.manager.draw()
    
        # Put the text on the screen.
        output = f"Score: {self.score} Checkpoint: {self.checkpoint}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.
        self.player_list.update()
        
        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.coin_list.update()
        self.medal_list.update()

        # Generate a list of all sprites that collided with the player.
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.coin_list)
        medals_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.medal_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        for medal in medals_hit_list:
            medal.remove_from_sprite_lists()
            self.medalMessage()
            self.checkpoint += 1

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def medalMessage(self):
        # The code in this function is run when we click the ok button.
        # The code below opens the message box and auto-dismisses it when done.
        self.message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=(
                "Instruction with Image"
            ),)
        self.manager.add(self.message_box)
    
def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()