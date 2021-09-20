# Author: Wai Kin Yong
# Date: 10/03/2021
# Description: Implementation of a Janggi Game. Contains a parent class Piece, and child Classes, Soldier, Cannon,
#              Chariot, Elephant, Horse, Guard and General representing the different units in Janggi, each child class
#              contains simple move generation to generate valid moves.
#              The board is represented by its own class Board, and the overall game is represented by the class
#              JanggiGame. JanggiGame will enable the Players to make moves, and will update the turn state and game
#              state if a checkmate is reached. In this implementation, perpetual check, position repetition, stalemate,
#              any kinds of draw mechanics are not implemented.


class Piece:
  """
  Represents a Piece in the Janggi Game. Contains 2 getter methods get_player and get_location for the 2 private data
  members respectively, and a setter method set_location.

  Piece serves as a parent class to be inherited by all the specific pieces class below. Should not be initialized on
  its own.
  """

  def __init__(self, player, location):
    """
    Initializes a Piece with two data members
    _player: The Player color the Piece belongs to, either 'blue' or 'red'.
    _location: Stores the location on the board that the Piece is at, in a list, with the format [row, col]
    """
    self._player = player
    self._location = location

  def get_player(self):
    """Returns the player color that the piece belongs to either 'blue' or 'red'"""
    return self._player

  def get_location(self):
    """Returns the current location of the Piece as a list, formatted as [row, col]"""
    return self._location

  def set_location(self, indexes):
    """Changes the location data for a piece"""
    self._location = indexes


class Soldier(Piece):
  """
  Represents a Soldier Piece.

  Soldiers may only move forward or sideways one point at a time. No backwards movement is allowed.

  Soldiers may also move along the diagonal lines the Palace.
  """

  def __init__(self, player, location):
    """
    Initializes a new Soldier object. Contains 2 private data members from Piece parent class, _player indicating the
    player that this Soldier belongs to, and _location storing the current location of this piece.
    """
    super().__init__(player, location)

  def move_generator(self, board):
    """
    Generates all valid moves for a particular Soldier object depending on the location it is at on the board. Moves
    that are blocked or out of the board will not be generated. Moves that leave the Player in check are generated, and
    will be validated in the JanggiGame make_move() method.
    """
    # Defines movement limits for Soldier piece depending on the player, both Blue and Red can only move forward one
    # square. No backwards movement is allowed. Left and right movement is allowed for both.
    player = self.get_player()
    location = self.get_location()
    col_move = [1, -1]              # Left and right movement of one square
    diagonal_moves = None
    if player == 'blue':
      row_move = -1
      if location in [[2, 3], [2, 5]]:    # Potential diagonal moves in the enemy Palace for Blue
        diagonal_moves = [[1, 4]]
      elif location == [1, 4]:
        diagonal_moves = [[0, 3], [0, 5]]
    else:
      row_move = 1
      if location in [[7, 3], [7, 5]]:    # Potential diagonal moves in the enemy Palace for Red
        diagonal_moves = [[8, 4]]
      elif location == [8, 4]:
        diagonal_moves = [[9, 3], [9, 5]]

    origin_row = location[0]
    origin_col = location[1]

    # Generates the destination indexes for a potential sideways move
    for move in col_move:
      if 0 <= origin_col + move <= 8:
        destination_piece = board[origin_row][origin_col + move]
      # Discard if move is out of board
        if destination_piece is None or destination_piece.get_player() != player:
          yield [origin_row, origin_col + move]

    # Generates the destination indexes for a potential vertical move
    # Discard if move is out of board
    if 0 <= origin_row + row_move <= 9:
      destination_piece = board[origin_row + row_move][origin_col]
      if destination_piece is None or destination_piece.get_player() != player:
          yield [origin_row + row_move, origin_col]

    # If Soldier is in opponent Palace, yield potential diagonal move
    if diagonal_moves is not None:
      for move in diagonal_moves:
        destination_piece = board[move[0]][move[1]]
        if destination_piece is None or destination_piece.get_player() != player:
            yield move


class Cannon(Piece):
  """
  Represents a Cannon Piece.

  Cannons may only move in four directions vertically and horizontally, by jumping over another Piece. The Piece to be
  jumped over cannot be another Cannon.

  Cannons also may not capture another Cannon.

  After having a Piece to jump over in any direction, the Cannon may move to any point behind the jumped Piece until it
  is blocked, or captures an enemy piece. The Cannon can only jump over a single Piece.

  The Cannon may move diagonally in the palace, with the same restriction that it needs to jump over another piece.
  """
  def __init__(self, player, location):
    """
    Initializes a new Cannon object. Contains 2 private data members from Piece parent class, _player indicating the
    player that this Cannon belongs to, and _location storing the current location of this piece.
    """
    super().__init__(player, location)

  def move_generator(self, board):
    """
    Generates all valid moves for a particular Cannon object depending on the location it is at on the board. Moves
    that are blocked or out of the board will not be generated. Moves that leave the Player in check are generated, and
    will be validated in the JanggiGame make_move() method.
    """
    player = self.get_player()
    location = self.get_location()

    origin_row = location[0]
    origin_col = location[1]

    diagonal_moves = None

    # Forward movement for Blue / Backward movement for Red
    for row in range(origin_row - 1, 0, -1):
      jumped = False
      jump_square = board[row][origin_col]
      # Finds a piece for the Cannon to jump over
      if jump_square is not None and type(jump_square) is not Cannon:
        jumped = True
        for jump_row in range(row - 1, -1, -1):
          destination_square = board[jump_row][origin_col]
          # Yields move if square is empty
          if destination_square is None:
            yield [jump_row, origin_col]
          # If square contains an enemy piece and it is not a Cannon, yield the move and break the loop since there are
          # no more moves
          elif destination_square.get_player() != player and type(destination_square) is not Cannon:
            yield [jump_row, origin_col]
            break
          else:
            break
      if jumped is True:
        break

    # Backwards movement for Blue / Forward movement for Red
    for row in range(origin_row + 1, 9):
      jumped = False
      jump_square = board[row][origin_col]
      if jump_square is not None and type(jump_square) is not Cannon:
        jumped = True
        for jump_row in range(row + 1, 10):
          destination_square = board[jump_row][origin_col]
          if destination_square is None:
            yield [jump_row, origin_col]
          elif destination_square.get_player() != player and type(destination_square) is not Cannon:
            yield [jump_row, origin_col]
            break
          else:
            break
      if jumped is True:
        break

    # Left movement for Blue / Right movement for Red
    for col in range(origin_col - 1, 0, -1):
      jumped = False
      jump_square = board[origin_row][col]
      if jump_square is not None and type(jump_square) is not Cannon:
        jumped = True
        for jump_col in range(col - 1, -1, -1):
          destination_square = board[origin_row][jump_col]
          if destination_square is None:
            yield [origin_row, jump_col]
          elif destination_square.get_player() != player and type(destination_square) is not Cannon:
            yield [origin_row, jump_col]
            break
          else:
            break
      if jumped is True:
        break

    # Right movement for Blue / Left movement for Red
    for col in range(origin_col + 1, 8):
      jumped = False
      jump_square = board[origin_row][col]
      if jump_square is not None and type(jump_square) is not Cannon:
        jumped = True
        for jump_col in range(col + 1, 9):
          destination_square = board[origin_row][jump_col]
          if destination_square is None:
            yield [origin_row, jump_col]
          elif destination_square.get_player() != player and type(destination_square) is not Cannon:
            yield [origin_row, jump_col]
            break
          else:
            break
      if jumped is True:
        break

    # If in Red's palace
    if location in [[2, 3], [0, 5]]:
      diagonal_moves = [[2, 3], [0, 5]]
    elif location in [[2, 5], [0, 3]]:
      diagonal_moves = [[2, 5], [0, 3]]
    # If in Blue's Palace
    elif location in [[7, 3], [9, 5]]:
      diagonal_moves = [[7, 3], [9, 5]]
    elif location in [[7, 5], [9, 3]]:
      diagonal_moves = [[7, 5], [9, 3]]

    # Diagonal movement for the Cannon
    if diagonal_moves is not None:
      diagonal_moves.remove(location)
      diagonal_moves = diagonal_moves[0]
      if 0 <= diagonal_moves[0] <= 2:
        jump_square = board[1][4]
      elif 7 <= diagonal_moves[0] <= 9:
        jump_square = board[8][4]

      # Checks if there is a valid piece for the Cannon to jump over
      if jump_square is not None and type(jump_square) is not Cannon:
        destination_square = board[diagonal_moves[0]][diagonal_moves[1]]
        # Checks if destination is empty or contains an enemy piece that is not a Cannon
        if destination_square is None or (destination_square.get_player() != player and type(destination_square) is not
                                          Cannon):
          yield diagonal_moves


class Chariot(Piece):
  """
  Represents a Chariot Piece.

  Chariots may move any distance in any of the four directions vertically or horizontally up to a point where it
  captures an enemy piece or is blocked by other pieces.

  Chariots may not jump over other units.

  Chariots in the Palace may move on the diagonal lines with similar restrictions to the above.
  """
  def __init__(self, player, location):
    """
    Initializes a new Chariot object. Contains 2 private data members from Piece parent class, _player indicating the
    player that this Chariot belongs to, and _location storing the current location of this piece.
    """
    super().__init__(player, location)

  def move_generator(self, board):
    """
    Generates all valid moves for a particular Chariot object depending on the location it is at on the board. Moves
    that are blocked or out of the board will not be generated. Moves that leave the Player in check are generated, and
    will be validated in the JanggiGame make_move() method.
    """
    player = self.get_player()
    location = self.get_location()

    origin_row = location[0]
    origin_col = location[1]

    diagonal_moves = None

    # Forward movement for Blue / Backward movement for Red
    for row in range(origin_row - 1, -1, -1):
      destination_square = board[row][origin_col]
      # Yield move if square is empty
      if destination_square is None:
        yield [row, origin_col]
      # Yield move and break if square contains an enemy unit since there are no more moves after capturing an enemy
      # piece
      elif destination_square.get_player() != player:
        yield [row, origin_col]
        break
      # If a friendly piece is found, breaks without yielding
      else:
        break

    # Backward movement for Blue / Forward movement for Red
    for row in range(origin_row + 1, 10):
      destination_square = board[row][origin_col]
      if destination_square is None:
        yield [row, origin_col]
      elif destination_square.get_player() != player:
        yield [row, origin_col]
        break
      else:
        break

    # Left movement for Blue / Right movement for Red
    for col in range(origin_col - 1, -1, -1):
      destination_square = board[origin_row][col]
      if destination_square is None:
        yield [origin_row, col]
      elif destination_square.get_player() != player:
        yield [origin_row, col]
        break
      else:
        break

    # Right movement for Blue / Left movement for Red
    for col in range(origin_col + 1, 9):
      destination_square = board[origin_row][col]
      if destination_square is None:
        yield [origin_row, col]
      elif destination_square.get_player() != player:
        yield [origin_row, col]
        break
      else:
        break

    # If in Red's palace
    if location in [[2, 3], [0, 5]]:
      diagonal_moves = [[2, 3], [1, 4], [0, 5]]
    elif location == [1, 4]:
      diagonal_moves = [[2, 3], [2, 5], [0, 3], [0, 5]]
    elif location in [[2, 5], [0, 3]]:
      diagonal_moves = [[2, 5], [1, 4], [0, 3]]
    # If in Blue's Palace
    elif location in [[7, 3], [9, 5]]:
      diagonal_moves = [[8, 4], [7, 3], [9, 5]]
    elif location == [8, 4]:
      diagonal_moves = [[7, 3], [7, 5], [9, 3], [9, 5]]
    elif location in [[7, 5], [9, 3]]:
      diagonal_moves = [[8, 4], [7, 5], [9, 3]]

    # Diagonal movement for a Chariot in either Palace
    if diagonal_moves is not None:
      diagonal_moves.remove(location)
      for move in diagonal_moves:
        destination_square = board[move[0]][move[1]]
        # Checks if destination is empty or contains an opponent Piece
        if destination_square is None:
          yield move
        elif destination_square.get_player() != player:
          yield move
          break


class Elephant(Piece):
  """
  Represents a Elephant Piece. Contains an init() method, and a move_generator() method to generate possible moves
  subject to the movement restrictions of the Elephant Class.

  Elephants may move 1 point in all four directions, then 2 points diagonally. The complete sequence is a single move.

  Elephants may not jump over other units, if at any point before the ending point there is a unit in the Elephant's
  path, the Elephant may not move there.
  """

  def __init__(self, player, location):
    """
    Initializes a new Elephant object. Contains 2 private data members from Piece parent class, _player indicating the
    player that this Elephant belongs to, and _location storing the current location of this piece.
    """
    super().__init__(player, location)

  def move_generator(self, board):
    """
    Generator method for the Elephant Class. Takes one parameter board, that is the current board state. board is used
    to check if there are any blocking pieces.

    The generator will yield moves from the current location of the Elephant Piece, for every point that a Elephant may
    move to.

    Elephants move 1 point sideways or vertically, then 2 points diagonally. Maximum of 8 possible moves available.

    The generator will only yield valid moves, and if a point on the board is blocked by a friendly piece, or the move
    will be out of the board, or there is a blocking piece in the path, it will not yield that move.
    """
    player = self.get_player()
    location = self.get_location()

    origin_row = location[0]
    origin_col = location[1]

    diagonal_move = [1, -1]
    diagonal_move_2 = [2, -2]

    # Upwards movement for Blue / Downwards movement for Red
    # Checks if the immediate point above Elephant is blocked
    if origin_row - 1 > 2 and board[origin_row - 1][origin_col] is None:
      destination_row = origin_row - 2
      # Checks if the first diagonal square is blocked
      for move in diagonal_move:
        if 1 <= origin_col + move <= 7:
          destination_piece = board[destination_row][origin_col + move]
          if destination_piece is None:
            # Checks if final destination point is blocked by own Piece
            for move_2 in diagonal_move_2:
              if 0 <= origin_col + move_2 <= 8 and 0 <= destination_row + 1 <= 9:
                destination_piece = board[destination_row - 1][origin_col + move_2]
                if destination_piece is None or destination_piece.get_player() != player:
                  yield [destination_row - 1, origin_col + move_2]

    # Downwards movement for Blue / Upwards movement for Red
    # Checks if the immediate point below Elephant is blocked
    if origin_row + 1 < 7 and board[origin_row + 1][origin_col] is None:
      destination_row = origin_row + 2
      # Checks if the first diagonal square is blocked
      for move in diagonal_move:
        if 1 <= origin_col + move <= 7:
          destination_piece = board[destination_row][origin_col + move]
          if destination_piece is None:
            # Checks if final destination point is blocked by own Piece
            for move_2 in diagonal_move_2:
              if 0 <= origin_col + move_2 <= 8 and 0 <= destination_row + 1 <= 9:
                destination_piece = board[destination_row + 1][origin_col + move_2]
                if destination_piece is None or destination_piece.get_player() != player:
                  yield [destination_row + 1, origin_col + move_2]

    # Leftwards movement for Blue / Rightwards movement for Red
    if origin_col - 1 > 2 and board[origin_row][origin_col - 1] is None:
      destination_col = origin_col - 2
      # Checks if the first diagonal square is blocked
      for move in diagonal_move:
        if 1 <= origin_row + move <= 8:
          destination_piece = board[origin_row + move][destination_col]
          if destination_piece is None:
            # Checks if final destination point is blocked by own Piece
            for move_2 in diagonal_move_2:
              if 0 <= origin_row + move_2 <= 9 and 0 <= destination_col - 1 <= 8:
                destination_piece = board[origin_row + move_2][destination_col - 1]
                if destination_piece is None or destination_piece.get_player() != player:
                  yield [origin_row + move_2, destination_col - 1]

    # Rightwards movement for Blue / Leftwards movement for Red
    if origin_col + 1 < 6 and board[origin_row][origin_col + 1] is None:
      destination_col = origin_col + 2
      # Checks if the first diagonal square is blocked
      for move in diagonal_move:
        if 1 <= origin_row + move <= 8:
          destination_piece = board[origin_row + move][destination_col]
          if destination_piece is None:
            # Checks if final destination point is blocked by own Piece
            for move_2 in diagonal_move_2:
              if 0 <= origin_row + move_2 <= 9 and 0 <= destination_col + 1 <= 8:
                destination_piece = board[origin_row + move_2][destination_col + 1]
                if destination_piece is None or destination_piece.get_player() != player:
                  yield [origin_row + move_2, destination_col + 1]


class Horse(Piece):
  """
  Represents a Horse Piece. Contains an init() method, and a move_generator() method to generate possible moves
  subject to the movement restrictions of the Horse Class.

  Horses move 1 point sideways or vertically, then 1 point diagonally. The complete sequence is a single move.

  Horses may not jump over other units, if at any point before the ending point there is a unit in the Horse's path, the
  Horse is blocked and may not move there.
  """

  def __init__(self, player, location):
    """
    Initializes a new Horse object. Contains 2 private data members from Piece parent class, _player indicating the
    player that this Horse belongs to, and _location storing the current location of this piece.
    """
    super().__init__(player, location)

  def move_generator(self, board):
    """
    Generator method for the Horse Class. Takes one parameter board, that is the current board state. board is used
    to check if there are any blocking pieces.

    The generator will yield moves from the current location of the Horse Piece, for every point that a Horse may
    move to.

    Horses move 1 point sideways or vertically, then 1 points diagonally. Maximum of 8 possible moves available.

    The generator will only yield valid moves, and if a point on the board is blocked by any piece, or the move
    will be out of the board, or there is a blocking piece in the path, it will not yield that move.
    """

    player = self.get_player()
    location = self.get_location()

    origin_row = location[0]
    origin_col = location[1]

    diagonal_move = [1, -1]

    # Upwards movement for Blue / Downwards movement for Red
    if origin_row - 1 > 1 and board[origin_row - 1][origin_col] is None:
      destination_row = origin_row - 2
      for move in diagonal_move:
        # Checks if the diagonal move is within the board
        if 0 <= origin_col + move <= 8:
          destination_piece = board[destination_row][origin_col + move]
          # Checks if destination is empty or contains an enemy piece to be captured and yields the move
          if destination_piece is None or destination_piece.get_player() != player:
            yield [destination_row, origin_col + move]

    # Downwards movement for Blue / Upwards movement for Red
    if origin_row + 1 < 8 and board[origin_row + 1][origin_col] is None:
      destination_row = origin_row + 2
      for move in diagonal_move:
        if 0 <= origin_col + move <= 8:
          destination_piece = board[destination_row][origin_col + move]
          if destination_piece is None or destination_piece.get_player() != player:
            yield [destination_row, origin_col + move]

    # Leftwards movement for Blue / Rightwards movement for Red
    if origin_col - 1 > 1 and board[origin_row][origin_col - 1] is None:
      destination_col = origin_col - 2
      for move in diagonal_move:
        if 0 <= origin_row + move <= 9:
          destination_piece = board[origin_row + move][destination_col]
          if destination_piece is None or destination_piece.get_player() != player:
            yield [origin_row + move, destination_col]

    # Rightwards movement for Blue / Leftwards movement for Red
    if origin_col + 1 < 7 and board[origin_row][origin_col + 1] is None:
      destination_col = origin_col + 2
      for move in diagonal_move:
        if 0 <= origin_row + move <= 9:
          destination_piece = board[origin_row + move][destination_col]
          if destination_piece is None or destination_piece.get_player() != player:
            yield [origin_row + move, destination_col]


class Guard(Piece):
  """
  Represents a Guard Piece. Contains an init() method, and a move_generator() method to generate possible moves
  subject to the movement restrictions of the Guard Class.

  Guards move 1 point along the lines in the Palace, and may not move outside of the Palace.

  Movement is either vertical or horizontal in four directions, and diagonal on certain points according to the lines
  in the Palace.
  """

  def __init__(self, player, location):
    """
    Initializes a new Guard object. Contains 2 private data members from Piece parent class, _player indicating the
    player that this Guard belongs to, and _location storing the current location of this piece.
    """
    super().__init__(player, location)

  def move_generator(self, board):
    """
    Generator method for the Guard Class. Takes one parameter board, that is the current board state. board is used to
    check if there are any blocking pieces.

    The generator will yield moves from the current location of the Guard Piece, one point sideways or forward.

    If the Guard is on a point where diagonal movement is possible, possible diagonal movement will also be generated.

    The generator will only yield valid moves, and if a point on the board is blocked by a friendly piece, or the move
    will be out of the Palace, it will not yield that move.
    """
    # Defines movement limits for Guard piece depending on the player, both Blue and Red can only move forward one
    # square. Left and right movement is allowed for both.
    player = self.get_player()
    location = self.get_location()
    move_list = [1, -1]              # Movement of one square
    diagonal_moves = None
    # If Guard is on any point with a diagonal path, sets diagonal_moves to a list of the possible diagonals moves
    if location in [[2, 3], [2, 5], [0, 3], [0, 5]]:
      diagonal_moves = [[1, 4]]
    elif location == [1, 4]:
      diagonal_moves = [[2, 3], [2, 5], [0, 3], [0, 5]]
    elif location in [[7, 3], [7, 5], [9, 3], [9, 5]]:
      diagonal_moves = [[8, 4]]
    elif location == [8, 4]:
      diagonal_moves = [[7, 3], [7, 5], [9, 3], [9, 5]]

    origin_row = location[0]
    origin_col = location[1]

    # Generates the destination indexes for a potential sideways move
    for move in move_list:
      # Discard if move is out of Palace columns
      if 3 <= origin_col + move <= 5:
        destination_piece = board[origin_row][origin_col + move]
        # If destination square is empty or contains an enemy piece to be captured, yields move
        if destination_piece is None or destination_piece.get_player() != player:
          yield [origin_row, origin_col + move]

    # Generates the destination indexes for a potential vertical move
    for move in move_list:
      # Discard if move is out of Palace rows
      if 7 <= origin_row + move <= 9 or 0 <= origin_row + move <= 2:
        destination_piece = board[origin_row + move][origin_col]
        if destination_piece is None or destination_piece.get_player() != player:
            yield [origin_row + move, origin_col]

    # If diagonal moves are available, check if not blocked and yield move
    if diagonal_moves is not None:
      for move in diagonal_moves:
        destination_piece = board[move[0]][move[1]]
        if destination_piece is None or destination_piece.get_player() != player:
            yield move


class General(Piece):
  """
  Represents a General Piece. Contains an init() method, and a move_generator() method to generate possible moves
  subject to the movement restrictions of the General Class.

  Generals move 1 point along the lines in the Palace, and may not move outside of the Palace.

  Movement is either vertical or horizontal in four directions, and diagonal on certain points according to the lines
  in the Palace.
  """

  def __init__(self, player, location):
    """
    Initializes a new General object. Contains 2 private data members from Piece parent class, _player indicating the
    player that this General belongs to, and _location storing the current location of this piece.
    """
    super().__init__(player, location)

  def move_generator(self, board):
    """
    Generator method for the General Class. Takes one parameter board, that is the current board state. board is used to
    check if there are any blocking pieces.

    The generator will yield moves from the current location of the General Piece, one point sideways or forward.

    If the General is on a point where diagonal movement is possible, possible diagonal movement will also be generated.

    The generator will only yield valid moves, and if a point on the board is blocked by a friendly piece, or the move
    will be out of the Palace, it will not yield that move.
    """
    # Defines movement limits for General piece depending on the player, both Blue and Red can only move forward one
    # square. No backwards movement is allowed. Left and right movement is allowed for both.
    player = self.get_player()
    location = self.get_location()
    move_list = [1, -1]              # Movement of one square
    diagonal_moves = None
    # If Guard is on any point with a diagonal path, sets diagonal_moves to a list of the possible diagonals moves
    if location in [[2, 3], [2, 5], [0, 3], [0, 5]]:
      diagonal_moves = [[1, 4]]
    elif location == [1, 4]:
      diagonal_moves = [[2, 3], [2, 5], [0, 3], [0, 5]]
    elif location in [[7, 3], [7, 5], [9, 3], [9, 5]]:
      diagonal_moves = [[8, 4]]
    elif location == [8, 4]:
      diagonal_moves = [[7, 3], [7, 5], [9, 3], [9, 5]]

    origin_row = location[0]
    origin_col = location[1]

    # Generates the destination indexes for a potential sideways move
    for move in move_list:
      # Discard if move is out of Palace columns
      if 3 <= origin_col + move <= 5:
        destination_piece = board[origin_row][origin_col + move]
        # If destination square is empty or contains an enemy piece to be captured, yields move
        if destination_piece is None or destination_piece.get_player() != player:
          yield [origin_row, origin_col + move]

    # Generates the destination indexes for a potential vertical move
    for move in move_list:
      # Discard if move is out of Palace rows
      if 7 <= origin_row + move <= 9 or 0 <= origin_row + move <= 2:
        destination_piece = board[origin_row + move][origin_col]
        if destination_piece is None or destination_piece.get_player() != player:
            yield [origin_row + move, origin_col]

    # If diagonal moves are available, check if not blocked and yield move
    if diagonal_moves is not None:
      for move in diagonal_moves:
        destination_piece = board[move[0]][move[1]]
        if destination_piece is None or destination_piece.get_player() != player:
            yield move


class Board:
  """
  Represents a Janggi Board. Contains 1 getter method get_board, and two method to move pieces move_piece and
  undo_move_piece, and a method to place the pieces on the board
  """
  def __init__(self):
    """Initializes an empty board. Represented by a 2D nested list structure"""
    self._board = [[None for _ in range(9)] for _ in range(10)]

  def initial_placement(self, player_blue, player_red):
    """
    Place pieces on the board for each player at the start of a game.
    Takes two input parameters:
    player_blue: The object representing the 'blue' Player
    player_red: The object representing the 'red' Player
    """
    # Gets the list of pieces that each player currently has at the start of the game, generals are stored separately
    placement_pieces = [player_blue.get_pieces(), player_red.get_pieces()]
    placement_generals = [player_blue.get_general(), player_red.get_general()]

    # Iterates through each Piece object in each list and place them in their initial location on the board
    for piece_list in placement_pieces:
      for piece in piece_list:
        location = piece.get_location()
        loc_row = location[0]
        loc_col = location[1]
        self._board[loc_row][loc_col] = piece

    # Iterates through the General objects in the list and place them in their initial location on the board
    for general in placement_generals:
      location = general.get_location()
      loc_row = location[0]
      loc_col = location[1]
      self._board[loc_row][loc_col] = general

  def get_board(self):
    """Returns the current board state"""
    return self._board

  def move_piece(self, origin_indexes, destination_indexes):
    """
    Moves a piece on the board from the origin_indexes to the destination_indexes
    Takes two parameters:
    origin_indexes: A list in the format [row, col], containing the index of the board where a Piece is to be moved from
    destination_indexes: A list in the same format as above, containing the index of the board where a Piece will be
    moved to
    """
    board = self.get_board()
    origin_piece = board[origin_indexes[0]][origin_indexes[1]]
    destination_piece = board[destination_indexes[0]][destination_indexes[1]]

    # Sets the location data member of the Piece to be captured to None, indicating that the Piece is off the board
    if destination_piece is not None:
      destination_piece.set_location(None)

    # Sets the location of the origin piece to the destination
    origin_piece.set_location(destination_indexes)

    # Moves the origin piece from the origin to the destination on the board
    board[destination_indexes[0]][destination_indexes[1]] = origin_piece
    board[origin_indexes[0]][origin_indexes[1]] = None

  def undo_move_piece(self, origin_indexes, destination_indexes, deleted_piece):
    """
    Undoes a move that was done previously.
    Takes 3 input parameters:
    origin_indexes: A list in the format [row, col], containing the indexes of the board where a Piece was moved from
    destination_indexes: A list in the same format as above, containing the indexes of the board where a Piece was
    moved to.
    deleted_piece: Contains the Piece object that was captured in a prior move. If no Piece was captured, this will be
    None.
    """
    board = self.get_board()
    origin_piece = board[destination_indexes[0]][destination_indexes[1]]
    # If there was a captured piece, set the location of the captured piece back to its original location
    if deleted_piece is not None:
      deleted_piece.set_location(destination_indexes)
    # Sets the location of the moved piece to its original location
    origin_piece.set_location(origin_indexes)

    # Replace both pieces to their original positions
    board[destination_indexes[0]][destination_indexes[1]] = deleted_piece
    board[origin_indexes[0]][origin_indexes[1]] = origin_piece


class JanggiGame:
  """Represents a Janggi Game"""
  def __init__(self):
    """
    Initializes a new Janggi Game. Contains 6 data members:
    _gameboard: Initializes and stores the Board object representing the game board of a Janggi Game
    _turn: Stores the Player's color whose turn it is to move. Either 'blue' or 'red'.
    _game_state: Stores the current game state. Can be 'UNFINISHED', 'BLUE_WON' or 'RED_WON'.
    _index_map: Generates and stores the dict containing the algebraic notations and their corresponding index values
    for their positions on the board
    _player_blue: Initializes and stores the Player object for the 'blue' player
    _player_red: Initializes and stores the Player object for the 'red' player
    """
    self._gameboard = Board()
    self._turn = 'blue'
    self._game_state = "UNFINISHED"
    self._index_map = self.generate_index_map()
    self._player_blue = Player('blue')
    self._player_red = Player('red')

    # Calls the method in _gameboard to place all the piece in their initial positions
    self._gameboard.initial_placement(self._player_blue, self._player_red)

  @staticmethod
  def generate_index_map():
    """
    Returns a dictionary that stores the algebraic notation as key's and its corresponding index values as a list
    in the value
    """
    index_map = {}
    col_track = 0

    # Creates the algebraic notation syntax in a list and iterates through them to store the corresponding index values
    for count in range(9):
      lst = [chr(ord('a') + count) + str(i) for i in range(1, 11)]
      row = 0
      col = col_track
      for element in lst:
        index_map[element] = [row, col]
        row += 1
      col_track += 1

    return index_map

  def get_game_state(self):
    """Returns the current game state. Either 'UNFINISHED', 'BLUE_WON' or 'RED_WON'."""
    return self._game_state

  def get_turn(self):
    """Returns the color of the Player whose turn it is to move. Either 'blue' or 'red'."""
    return self._turn

  def get_index_map(self):
    """Returns the dict containing the index map for the algebraic notation and the corresponding index values"""
    return self._index_map

  def get_gameboard(self):
    """Returns the Board object"""
    return self._gameboard

  def get_player_blue(self):
    """Returns the Player object for the 'blue' Player"""
    return self._player_blue

  def get_player_red(self):
    """Returns the Player object for the 'red' Player"""
    return self._player_red

  def make_move(self, origin, destination):
    """
    Takes two input parameters:
    origin: The position that a Piece is to be moved from in algebraic notation
    destination: The position that a Piece will be moved to in algebraic notation
    Attempts to make a move from one position to another. make_move() contains various checks to ensure that the move
    that is being made is valid and will not leave the player in check.

    At the end of a successful move, will check if the other player is in checkmate and updates the game status
    accordingly.

    If no checkmate is found, then the turn is changed and make_move returns True.

    If any check fails, and the attempted move is invalid, returns False
    """
    # Checks if the game is still in play with no winner
    if self.get_game_state() != 'UNFINISHED':
      return False

    # Checks if the algebraic notations are valid
    index_map = self.get_index_map()
    if origin not in index_map or destination not in index_map:    # Checks if the algebraic notations are valid
      return False

    player = self.get_turn()
    # Checks if player intends to pass
    # If player is not in check, then a pass is valid
    if origin == destination:
      if self.is_in_check(player) is False:
        self.change_turn()
        return True
      else:
        return False

    board = self.get_gameboard()
    board_state = board.get_board()
    origin_indexes = index_map[origin]
    origin_piece = board_state[origin_indexes[0]][origin_indexes[1]]
    destination_indexes = index_map[destination]
    destination_piece = board_state[destination_indexes[0]][destination_indexes[1]]

    # Checks if the origin square is empty
    if origin_piece is None:
      return False

    # Checks if the Piece in the first input square belongs to the current Player (turn to move)
    if self.check_turn(origin_piece) is False:
      return False

    # Generates the possible move and checks if the destination is generated. If not then the destination is not a valid
    # move and returns False
    move_list = origin_piece.move_generator(board_state)
    while True:
      try:
        move = next(move_list)
        if move == destination_indexes:
          break
      except StopIteration:
        return False

    # Moves Piece on board and updates the location of the Piece
    board.move_piece(origin_indexes, destination_indexes)

    if self.is_in_check(player) is True:
      board.undo_move_piece(origin_indexes, destination_indexes, destination_piece)
      return False

    # If move is valid, checks if the opponent's General is in check
    if player == 'blue':
      opponent = 'red'
    else:
      opponent = 'blue'

    # If opponent's General is in check, check if the opponent has no more moves and is in check mate
    if self.is_in_check(opponent) is True:
      if self.is_checkmate(opponent) is True:
        self.change_win()               # Changes _game_state to the player that won

    # Change the turn to the other Player's color and returns True
    self.change_turn()
    return True

  def is_in_check(self, player_color):
    """
    Takes one input parameter, player_color. Input parameter is either 'blue' or 'red'.
    Will check if the Player whose color is the input parameter is in check.
    Returns True if Player is in check and False if not.
    """
    # Gets the game board and initializes the value for opponent and player depending on the input parameter
    board = self.get_gameboard().get_board()
    if player_color == 'blue':
      opponent = self.get_player_red()
      player = self.get_player_blue()
    else:
      opponent = self.get_player_blue()
      player = self.get_player_red()

    # Gets the list containing the Opponent's Piece objects and the location of the Player's General object
    opponent_pieces = opponent.get_pieces()
    player_general_loc = player.get_general().get_location()

    # Iterates through each Piece object in the List
    for pieces in opponent_pieces:
      # Checks if the Piece exists on the Board and calls move_generator() for the Piece
      # Ignores the Guard Piece since it cannot check an opponent's General as it is confined to the Palace
      if pieces.get_location() is not None and type(pieces) is not Guard:
        move_generator = pieces.move_generator(board)
        # Iterates through the generator and checks if any of the moves matches the Player's General object location,
        # the Player is in check and returns True
        while True:
          try:
            move = next(move_generator)
            if move == player_general_loc:
              return True
          # If the generator is exhausted, breaks the while Loop and moves on to the next Piece
          except StopIteration:
            break

    # If all generated moves do not match the Player's General object location, then the Player is not in check and
    # returns False
    return False

  def is_checkmate(self, player_color):
    """Checks if a player is in checkmate. Returns True if checkmate and False if not"""

    board_obj = self.get_gameboard()
    board = board_obj.get_board()
    if player_color == 'blue':
      player = self.get_player_blue()
    else:
      player = self.get_player_red()

    # Gets all the Pieces for the player in check
    player_pieces = player.get_pieces()
    player_pieces.append(player.get_general())

    # Iterates through all the Pieces the player has, including the General
    for pieces in player_pieces:
      piece_location = pieces.get_location()
      # Generates all the moves available and checks if any move removes the check on the player's General
      if piece_location is not None:
        move_generator = pieces.move_generator(board)
        while True:
          try:
            move = next(move_generator)
            destination_piece = board[move[0]][move[1]]
            board_obj.move_piece(piece_location, move)
            # If the check is removed, then undo the move and return False since the player is not in checkmate and a
            # valid move is available
            if self.is_in_check(player_color) is False:
              board_obj.undo_move_piece(piece_location, move, destination_piece)
              return False
            # If the check is not removed, undo the move and continues checking the other moves until all moves have
            # been exhausted.
            else:
              board_obj.undo_move_piece(piece_location, move, destination_piece)
          except StopIteration:
            break

    # After all moves generated has been exhausted and the player is still in check, then the player is in checkmate
    # and the method returns True
    return True

  def check_turn(self, piece):
    """
    Checks if the player whose piece is attempting to move belongs to the current player.
    Returns True if the Piece belongs to the player that is supposed to move in the current turn.
    Returns False if not.
    """
    current_turn = self.get_turn()
    if current_turn == piece.get_player():
      return True
    else:
      return False

  def change_turn(self):
    """Checks the current turn and changes it to the other player."""
    turn = self.get_turn()
    if turn == 'blue':
      self._turn = 'red'
    else:
      self._turn = 'blue'

  def change_win(self):
    """
    Checks which Player has made a move and change the _game_state data member to 'BLUE_WON' or 'RED_WON'.
    To be used to change the game_state when there is a checkmate
    """
    turn = self.get_turn()
    if turn == 'blue':
      self._game_state = 'BLUE_WON'
    else:
      self._game_state = 'RED_WON'


class Player:
  """
  Class representing a Player.
  Contains method _generate_pieces to initialize all default Pieces in with their starting locations according to their
  player color.
  A _set_general method to set the General for each Player.
  And two getter methods get_pieces, returning a list of Piece objects that a Player has. And get_general, returning
  the General object for that Player.
  """
  def __init__(self, player_color):
    """
    Initializes a new player and the pieces.
    Contains 3 private data members:
    _color: Stores the Player's color. Either 'blue' or 'red'
    _general: Stores the General object belonging to the Player
    _pieces: Initialized as an empty list, stores all the other Pieces belonging to the Player in the list except
    the General
    """
    self._color = player_color
    self._general = None
    self._pieces = []

    self._generate_pieces(player_color)

  def get_pieces(self):
    """Returns the list of pieces a player has"""
    return self._pieces

  def get_general(self):
    """Returns the general object for a player"""
    return self._general

  def _set_general(self, general):
    """Sets the _general data member to the General object"""
    self._general = general

  def _generate_pieces(self, player):
    """Initializes all the Pieces that a player has at the start of the game"""

    # Generate default locations for each piece
    if player == 'blue':
      soldiers_loc = [[6, 0], [6, 2], [6, 4], [6, 6], [6, 8]]
      cannon_loc = [[7, 1], [7, 7]]
      general_loc = [8, 4]
      chariot_loc = [[9, 0], [9, 8]]
      elephant_loc = [[9, 1], [9, 6]]
      horse_loc = [[9, 2], [9, 7]]
      guard_loc = [[9, 3], [9, 5]]
    elif player == 'red':
      soldiers_loc = [[3, 0], [3, 2], [3, 4], [3, 6], [3, 8]]
      cannon_loc = [[2, 1], [2, 7]]
      general_loc = [1, 4]
      chariot_loc = [[0, 0], [0, 8]]
      elephant_loc = [[0, 1], [0, 6]]
      horse_loc = [[0, 2], [0, 7]]
      guard_loc = [[0, 3], [0, 5]]

    # Initializes each piece with the default location according to the player color above and adds them to _pieces
    for loc in soldiers_loc:
      soldier = Soldier(player, loc)
      self._pieces.append(soldier)

    for loc in cannon_loc:
      cannon = Cannon(player, loc)
      self._pieces.append(cannon)

    for loc in chariot_loc:
      chariot = Chariot(player, loc)
      self._pieces.append(chariot)

    for loc in elephant_loc:
      elephant = Elephant(player, loc)
      self._pieces.append(elephant)

    for loc in horse_loc:
      horse = Horse(player, loc)
      self._pieces.append(horse)

    for loc in guard_loc:
      guard = Guard(player, loc)
      self._pieces.append(guard)

    # Initializes the General and sets _general to it
    general = General(player, general_loc)
    self._set_general(general)
