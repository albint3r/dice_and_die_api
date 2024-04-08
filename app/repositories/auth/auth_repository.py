from pydantic import BaseModel

from app.db.db import _DataBase  # noqa
from app.domain.analytics.entities.single_play_history import SinglePlayHistory
from app.domain.auth.entities.bank_account import BankAccount
from app.domain.auth.entities.user import User
from app.domain.auth.entities.user_level import UserLevel
from app.domain.auth.entities.user_rank import UserRank
from app.domain.auth.errors.errors import UserLevelNotExist, NoUserInRanking
from app.domain.game.entities.play_history import PlayHistory


class AuthRepository(BaseModel):
    """Authenticated repository"""
    db: _DataBase

    def get_user(self, email: str) -> User:
        """Get the user from the database"""
        query = 'SELECT * FROM users WHERE email=%s;'
        result = self.db.query(query, (email,), fetch_all=False)
        if result:
            return User(**result)

    def get_user_by_id(self, user_id: str) -> User | None:
        """Get the user from the database"""
        query = 'SELECT * FROM users WHERE user_id=%s;'
        result = self.db.query(query, (user_id,), fetch_all=False)
        if result:
            return User(**result)

    def create_user(self, email: str, name: str, password: str | bytes) -> None:
        """Create a new user"""
        query = "INSERT INTO users (email, name, password) VALUES (%s, %s, %s);"
        self.db.execute(query, (email, name, password))

    def delete_user(self, user_id: str) -> None:
        """Delete a user by user_id"""
        query = "DELETE FROM users WHERE user_id=%s;"
        self.db.execute(query, (user_id,))

    def get_user_level(self, user_id: str) -> UserLevel:
        """Get the User Level by the user id."""
        query = "SELECT * FROM users_levels WHERE user_id=%s;"
        result = self.db.query(query, (user_id,), fetch_all=False)
        if result:
            return UserLevel(**result)
        raise UserLevelNotExist('[User] ID no match with the User Level Table Information.')

    def create_user_level(self, user_id: str) -> None:
        """Create a new User Level Item"""
        query = "INSERT INTO users_levels (user_id) VALUES (%s);"
        self.db.execute(query, (user_id,))

    def get_user_bank_account(self, user_id: str) -> BankAccount:
        """Get the bank account of a user"""
        query = "SELECT * FROM bank_accounts WHERE user_id=%s;"
        result = self.db.query(query, (user_id,), fetch_all=False)
        if result:
            return BankAccount(**result)

    def create_user_bank_account(self, user_id: str) -> None:
        """Create a new bank account for a user"""
        query = "INSERT INTO bank_accounts (user_id) VALUES (%s);"
        self.db.execute(query, (user_id,))

    def update_user_name_and_last_name(self, user_id: str, name: str, last_name: str) -> None:
        """Update in the db the name and last name of the user id."""
        query = "UPDATE users SET name=%s, last_name=%s WHERE user_id=%s;"
        self.db.execute(query, (name, last_name, user_id))

    def get_users_ranking(self) -> list[UserRank]:
        """Update in the db the name and last name of the user id."""
        query = """
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY us.level DESC, us.exp_points DESC, u.name ASC) AS ranking,
                    u.user_id,
                    u.name, 
                    u.last_name, 
                    us.level, 
                    us.exp_points, 
                    us.rank_id
                FROM users AS u
                JOIN users_levels AS us ON us.user_id = u.user_id
                ORDER BY us.level DESC, us.exp_points DESC, u.name ASC
                limit 20;
            """
        result = self.db.query(query, (), fetch_all=True)
        if result:
            return [UserRank(**user) for user in result]
        raise NoUserInRanking('User not exit.')

    def get_user_ranking(self, user_id: str) -> UserRank:
        query = """
                SELECT * FROM(SELECT 
                        ROW_NUMBER() OVER (ORDER BY us.level DESC, us.exp_points DESC, u.name ASC) AS ranking,
                        u.name, 
                        u.user_id,
                        u.last_name, 
                        us.level, 
                        us.exp_points, 
                        us.rank_id
                    FROM users AS u
                    JOIN users_levels AS us ON us.user_id = u.user_id
                    ORDER BY us.level DESC, us.exp_points DESC, u.name ASC
                    ) AS subquery_alias
                WHERE user_id=%s;
            """
        values = (user_id,)
        result = self.db.query(query, values)
        if result:
            return UserRank(**result)
        raise NoUserInRanking('There is not user in the ranking leader. Crear user first')

    def get_users_ranking_by_rank(self, rank_id: int) -> list[UserRank]:
        query = """
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY us.level DESC, us.exp_points DESC, u.name ASC) AS ranking,
                    u.user_id,
                    u.name, 
                    u.last_name, 
                    us.level, 
                    us.exp_points, 
                    us.rank_id
                FROM users AS u
                JOIN users_levels AS us ON us.user_id = u.user_id
                WHERE rank_id=%s
                ORDER BY us.level DESC, us.exp_points DESC, u.name ASC
                limit 100;
            """
        values = (rank_id,)
        results = self.db.query(query, values, fetch_all=True)
        if results:
            return [UserRank(**result) for result in results]
        raise NoUserInRanking('There is not user in the ranking leader. Crear user first')

    def get_user_ranking_by_rank(self, rank_id: int, user_id: str) -> UserRank:
        query = """
                SELECT * FROM(SELECT 
                    ROW_NUMBER() OVER (ORDER BY us.level DESC, us.exp_points DESC, u.name ASC) AS ranking,
                    u.name, 
                    u.user_id,
                    u.last_name, 
                    us.level, 
                    us.exp_points, 
                    us.rank_id
                FROM users AS u
                JOIN users_levels AS us ON us.user_id = u.user_id
                WHERE rank_id=%s
                ORDER BY us.level DESC, us.exp_points DESC, u.name ASC
                ) AS subquery_alias
                WHERE user_id=%s;
            """
        values = (rank_id, user_id)
        result = self.db.query(query, values)
        if result:
            return UserRank(**result)
        raise NoUserInRanking('There is not user in the ranking league leader. Crear user first')

    def update_user_level(self, user_level: UserLevel) -> None:
        """Update the level and experience points of the user level"""
        query = "UPDATE users_levels SET " \
                "level = %s, " \
                "exp_points = %s, " \
                "next_level_points = %s, " \
                "rank_id = %s " \
                "WHERE user_id = %s;"
        values = (user_level.level, user_level.exp_points, user_level.next_level_points, user_level.rank_id,
                  user_level.user_id)
        self.db.execute(query, values)

    def update_user_bank_account_amount(self, user_id: str, amount: float) -> None:
        query = """UPDATE bank_accounts SET amount=%s WHERE user_id=%s;"""
        values = (amount, user_id)
        self.db.execute(query, values)

    def save_user_play_history(self, user: User, play_history: PlayHistory) -> None:
        query = """INSERT INTO users_play_history (user_id, play_history_id) VALUES (%s, %s);"""
        values = (user.user_id, str(play_history.play_history_id))
        self.db.execute(query, values)

    def save_game_history(self, play_history: PlayHistory) -> None:
        """Save the game match result"""
        query = """INSERT INTO play_history 
                        (creation_date, play_history_id, duration, p1, p1_score, 
                        p1_col_1_0, p1_col_1_1, p1_col_1_2, p1_col_2_0, p1_col_2_1, p1_col_2_2, 
                        p1_col_3_0, p1_col_3_1, p1_col_3_2, p2, p2_score, p2_col_1_0, p2_col_1_1, 
                        p2_col_1_2, p2_col_2_0, p2_col_2_1, p2_col_2_2, p2_col_3_0, p2_col_3_1, p2_col_3_2) 
                        VALUES (%s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s);"""
        values = (
            play_history.creation_date,
            str(play_history.play_history_id),
            play_history.duration,
            play_history.p1,
            play_history.p1_score,
            play_history.p1_col_1_0,
            play_history.p1_col_1_1,
            play_history.p1_col_1_2,
            play_history.p1_col_2_0,
            play_history.p1_col_2_1,
            play_history.p1_col_2_2,
            play_history.p1_col_3_0,
            play_history.p1_col_3_1,
            play_history.p1_col_3_2,
            play_history.p2,
            play_history.p2_score,
            play_history.p2_col_1_0,
            play_history.p2_col_1_1,
            play_history.p2_col_1_2,
            play_history.p2_col_2_0,
            play_history.p2_col_2_1,
            play_history.p2_col_2_2,
            play_history.p2_col_3_0,
            play_history.p2_col_3_1,
            play_history.p2_col_3_2
        )
        self.db.execute(query, values)

    def save_single_play_history(self, single_game_history: SinglePlayHistory) -> None:
        """Save the game match result"""
        query = """INSERT single_play_history 
                        (creation_date, game_id, p1_score, 
                        p1_col_1_0, p1_col_1_1, p1_col_1_2, p1_col_2_0, p1_col_2_1, p1_col_2_2, 
                        p1_col_3_0, p1_col_3_1, p1_col_3_2, p2_score, p2_col_1_0, p2_col_1_1, 
                        p2_col_1_2, p2_col_2_0, p2_col_2_1, p2_col_2_2, p2_col_3_0, p2_col_3_1, p2_col_3_2,
                        dice_result, column_index) 
                        VALUES (%s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s 
                                );"""
        values = (
            single_game_history.creation_date,
            single_game_history.game_id,
            single_game_history.p1_score,
            single_game_history.p1_col_1_0,
            single_game_history.p1_col_1_1,
            single_game_history.p1_col_1_2,
            single_game_history.p1_col_2_0,
            single_game_history.p1_col_2_1,
            single_game_history.p1_col_2_2,
            single_game_history.p1_col_3_0,
            single_game_history.p1_col_3_1,
            single_game_history.p1_col_3_2,
            single_game_history.p2_score,
            single_game_history.p2_col_1_0,
            single_game_history.p2_col_1_1,
            single_game_history.p2_col_1_2,
            single_game_history.p2_col_2_0,
            single_game_history.p2_col_2_1,
            single_game_history.p2_col_2_2,
            single_game_history.p2_col_3_0,
            single_game_history.p2_col_3_1,
            single_game_history.p2_col_3_2,
            single_game_history.dice_result,
            single_game_history.column_index
        )
        self.db.execute(query, values)
