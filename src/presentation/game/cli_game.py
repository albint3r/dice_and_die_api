from src.domain.game.i_game_facade import IGameFacade


def run_game(facade: IGameFacade):
    g = facade.new_game()
    start_player = facade.select_player_start(g)
    g.set_current_player(start_player)
    while not g.is_finish:
        print(g.p1)
        print(g.p2)
        # Roll the dice
        g.current_player.roll_dice()
        print(f"Die result: {g.current_player.die_result}")
        # Validate until the user put the value in a valid column
        while True:
            col_index = facade.select_column(player=g.current_player)
            if g.current_player.can_add_to_board_col(col_index):
                die_val = g.current_player.die_result
                if g.can_destroy_opponent_target_column(col_index, die_val):
                    g.destroy_opponent_target_column(col_index, die_val)
                g.current_player.add_dice_in_board_col(col_index, die_val)
                break
        if g.is_finish:
            print('Game is finish')
            break
        next_player = g.get_inverse_player()
        print('*-' * 100)
        g.set_current_player(next_player)
