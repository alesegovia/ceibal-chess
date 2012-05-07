#
#    Ceibal Chess - A chess activity for Sugar.
#    Copyright (C) 2009 Alejandro Segovia <asegovi@gmail.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
import unittest
from board import Board, RIGHT, LEFT
from piece import Move, EnPassant, Castling, Crowning, Pawn, Knight, Queen, Rook, King

class PawnTest(unittest.TestCase):
	'''Class for testing a pawn's moves'''

	def test_basic_white_moves(self):
		'''Test basic white pawn movement (step and double-step).'''
		board = Board(10, 10)
		pawn = Pawn(board.white)

		i, j = 1, 6
		board[i, j].piece = pawn

		moves = pawn.get_moves((i, j), board)

		self.assertEquals(len(moves), 2)
		self.assertTrue(Move((i,j), (i,j-1)) in moves)
		self.assertTrue(Move((i,j), (i,j-2)) in moves)

	def test_en_passant_right(self):
		'''Test en passant for black pawn.'''
		board = Board(10, 10)
		white_pawn = Pawn(board.white)
		black_pawn = Pawn(board.black)

		board[4, 4].piece = black_pawn
		board[5, 6].piece = white_pawn

		board.perform_move(Move((5,6), (5,4)))
		moves = black_pawn.get_moves((4, 4), board)

		self.assertEquals(2, len(moves))
		self.assertTrue(Move((4,4),(4,5)) in moves)
		self.assertTrue(EnPassant((4,4), RIGHT, board.black) in moves)

	def test_en_passant_left(self):
		'''Test en passant for black pawn.'''
		board = Board(10, 10)
		white_pawn = Pawn(board.white)
		black_pawn = Pawn(board.black)

		board[4, 4].piece = black_pawn
		board[3, 6].piece = white_pawn

		board.perform_move(Move((3,6), (3,4)))
		moves = black_pawn.get_moves((4, 4), board)

		self.assertEquals(2, len(moves))
		self.assertTrue(Move((4,4),(4,5)) in moves)
		self.assertTrue(EnPassant((4,4), LEFT, board.black) in moves)

	def test_white_attack_move(self):
		'''Test attack move for white pawn.'''
		board = Board(10, 10)
		white_pawn = Pawn(board.white)
		black_pawn = Pawn(board.black)

		i, j = 1, 6
		board[i, j].piece = white_pawn
		board[i-1, j-1].piece = black_pawn
		board[i+1, j-1].piece = black_pawn

		moves = white_pawn.get_moves((i, j), board)

		self.assertEquals(4, len(moves))
		self.assertTrue(Move((i,j),(i-1,j-1)) in moves)
		self.assertTrue(Move((i,j),(i+1,j-1)) in moves)

	def test_white_crowning(self):
		'''Test white crowning.'''
		board = Board(10, 10)
		pawn = Pawn(board.white)

		i, j = 1, 1
		board[i, j].piece = pawn

		moves = pawn.get_moves((i, j), board)

		self.assertEquals(len(moves), 1)
		self.assertTrue(moves[0].type == "Crowning")

	def test_white_crowning_with_type(self):
		'''Test white crowning.'''
		board = Board(10, 10)
		pawn = Pawn(board.white)

		i, j = 1, 1
		board[i, j].piece = pawn

		moves = pawn.get_moves((i, j), board, type="R")

		self.assertEquals(len(moves), 1)
		self.assertTrue(moves[0].type == "Crowning")
		self.assertTrue(moves[0].type == "Crowning")
		self.assertTrue(isinstance(moves[0].piece, Rook))

	def test_white_crowning_attack(self):
		'''Test white crowning attack.'''
		board = Board(10, 10)
		pawn = Pawn(board.white)
		rook = Rook(board.black)

		i, j = 1, 1
		board[i, j].piece = pawn
		board[0, 0].piece = rook

		moves = pawn.get_moves((i, j), board)

		self.assertEquals(2, len(moves))
		self.assertTrue(Crowning((1,1),(1,0),Queen(board.white)) in moves)
		self.assertTrue(Crowning((1,1),(0,0),Queen(board.white)) in moves)

class KnightTest(unittest.TestCase):
	'''Class for testing the knight's moves'''

	def test_basic_knight_moves(self):
		'''Test a knight's basic moves'''
		board = Board(10, 10)
		knight = Knight(board.white)

		i, j = 3, 4
		board[i, j].piece = knight

		moves = knight.get_moves((i, j), board)

		self.assertEquals(len(moves), 8)

	def test_knight_near_edge(self):
		'''Test a knight's moves when near an edge of the board'''
		board = Board(10, 10)
		knight = Knight(board.white)

		i, j = 0, 4
		board[i, j].piece = knight

		moves = knight.get_moves((i, j), board)

		self.assertEquals(len(moves), 4)

class EqualityTest(unittest.TestCase):
	'''Test for move equality'''

	def test_move_equality(self):
		'''Test Move instance equality'''
		m1 = Move((0, 0), (1, 1))
		m2 = Move((0, 0), (1, 1))
		self.assertEquals(m1, m2)

	def test_castling_equality(self):
		'''Test Castling instance equality'''
		board = Board()
		m1 = Castling("left", board.white)
		m2 = Castling("left", board.white)
		self.assertEquals(m1, m2)
	
	def test_crowning(self):
		'''Test Crowning instance equality'''
		board = Board()
		queen = Queen(board.white)
		m1 = Crowning((0,1),(0,0), queen)
		m2 = Crowning((0,1),(0,0), queen)
		self.assertEquals(m1, m2)

class MovementTest(unittest.TestCase):
	'''Test piece movements'''

	def test_move_instance(self):
		'''Test Move instance's data storage'''
		fro = 1,2
		to = 3,4
		m = Move(fro, to)

		self.assertEquals(m.fro, fro)
		self.assertEquals(m.to, to)

	def test_queen_horizontal_move_blocked(self):
		'''Test the Queen's horizontal move when blocked by a piece from the
		same owner.'''
		board = Board(10, 10)
		queen = Queen(board.white)
		pawn = Pawn(board.white)

		i, j = 0, 4
		board[i, j].piece = queen
		board[i+2, j].piece = pawn

		moves = queen.get_moves((i, j), board)

		self.assertTrue(Move((i,j), (i-1,j)) not in moves)
		self.assertTrue(Move((i,j), (i+1,j)) in moves)
		self.assertTrue(Move((i,j), (i+2,j)) not in moves)
		self.assertTrue(Move((i,j), (i+3,j)) not in moves)

	def test_queen_moves(self):
		'''Test the rook's moves unblocked'''
		board = Board(10, 10)
		queen = Queen(board.white)

		i, j = 4, 4
		board[i, j].piece = queen
		moves = queen.get_moves((i, j), board)

		self.assertTrue(Move((i,j),(i,0)) in moves)
		self.assertTrue(Move((i,j),(i,7)) in moves)
		self.assertTrue(Move((i,j),(0,j)) in moves)
		self.assertTrue(Move((i,j),(7,j)) in moves)
		self.assertTrue(Move((i,j),(i+1,j+1)) in moves)
		self.assertTrue(Move((i,j),(i+1,j-1)) in moves)
		self.assertTrue(Move((i,j),(i-1,j+1)) in moves)
		self.assertTrue(Move((i,j),(i-1,j-1)) in moves)

	def test_rook_moves(self):
		'''Test the rook's moves unblocked'''
		board = Board(10, 10)
		rook = Rook(board.white)

		i, j = 4, 4
		board[i, j].piece = rook
		moves = rook.get_moves((i, j), board)

		self.assertTrue(Move((i,j),(i,0)) in moves)
		self.assertTrue(Move((i,j),(i,7)) in moves)
		self.assertTrue(Move((i,j),(0,j)) in moves)
		self.assertTrue(Move((i,j),(7,j)) in moves)

class CastlingTest(unittest.TestCase):
	'''Test the king's castling move.'''

	def test_castling_no_moves(self):
		'''Test castling when neither the king nor the rook's have moved.'''
		board = Board(10, 10)
		king = King(board.white)
		rook_l = Rook(board.white)
		rook_r = Rook(board.white)

		board[0, 7].piece = rook_l
		board[7, 7].piece = rook_r
		board[4, 7].piece = king

		moves = king.get_moves((4, 7), board)

		self.assertTrue(Castling("left",board.white) in moves)
		self.assertTrue(Castling("right",board.white) in moves)

	def test_castling_forbidden_king_moved(self):
		'''Test that castling is forbidden once the king moved.'''
		board = Board(10, 10)
		king = King(board.white)
		rook_l = Rook(board.white)
		rook_r = Rook(board.white)

		board[0, 7].piece = rook_l
		board[7, 7].piece = rook_r
		board[4, 7].piece = king

		moves = king.get_moves((4, 7), board)
		move = Move((4,7),(5,7))
		self.assertTrue(move in moves)
		move.perform(board)

		moves = king.get_moves((4, 7), board)
		self.assertFalse(Castling("left",board.white) in moves)
		self.assertFalse(Castling("right",board.white) in moves)

	def test_castling_forbidden_rook_moved(self):
		'''Test that castling is forbidden once the rook moved.'''
		board = Board(10, 10)
		king = King(board.white)
		rook_l = Rook(board.white)
		rook_r = Rook(board.white)

		board[0, 7].piece = rook_l
		board[7, 7].piece = rook_r
		board[4, 7].piece = king

		moves = king.get_moves((4, 7), board)
		self.assertTrue(Castling("left",board.white) in moves)
		self.assertTrue(Castling("right",board.white) in moves)

		move = Move((0,7),(1,7))
		self.assertTrue(move in rook_l.get_moves((0,7),board))
		move.perform(board)

		moves = king.get_moves((4, 7), board)
		self.assertFalse(Castling("left",board.white) in moves)
		self.assertTrue(Castling("right",board.white) in moves)

		move = Move((7,7),(6,7))
		self.assertTrue(move in rook_r.get_moves((7,7),board))
		move.perform(board)

		moves = king.get_moves((4, 7), board)
		self.assertFalse(Castling("left",board.white) in moves)
		self.assertFalse(Castling("right",board.white) in moves)

	def test_castling_permitted_after_undo(self):
		board = Board(10, 10)
		king = King(board.white)
		rook_l = Rook(board.white)
		rook_r = Rook(board.white)

		board[0, 7].piece = rook_l
		board[7, 7].piece = rook_r
		board[4, 7].piece = king

		moves = king.get_moves((4, 7), board)
		self.assertTrue(Castling("left",board.white) in moves)
		self.assertTrue(Castling("right",board.white) in moves)

		move = Move((0,7),(1,7))
		self.assertTrue(move in rook_l.get_moves((0,7),board))
		move.perform(board)
		move.undo(board)

		moves = king.get_moves((4, 7), board)
		self.assertTrue(Castling("left",board.white) in moves)
		self.assertTrue(Castling("right",board.white) in moves)

class PerformUndoMoveTest(unittest.TestCase):
	'''Test performing moves and undoing them on a board.'''

	def test_move_perform_undo(self):
		'''Test performing a move and then undoing it.'''
		#set up:
		board = Board(10, 10)

		pawn = Pawn(board.white)
		i, j = 0, 6
		board[i, j].piece = pawn

		move = pawn.get_moves((i, j), board)[0]

		#initial conditions:
		self.assertTrue(not board[i, j-1].piece)
		self.assertTrue(board[i, j].piece)

		#test performing the move:
		move.perform(board)
		self.assertTrue(board[i, j-1].piece)
		self.assertTrue(not board[i, j].piece)

		self.assertTrue(not move.dst_piece)
		self.assertTrue(move.performed)

		#test undoing the move:
		move.undo(board)
		self.assertTrue(not board[i, j-1].piece)
		self.assertTrue(board[i, j].piece)
		self.assertTrue(not move.performed)

	def test_castling_white_left(self):
		'''Test performing a castling move to the left and then undoing it.'''
		board = Board(10, 10)
		board.current_turn = board.white
		king = King(board.white)
		rook = Rook(board.white)

		ki, ri, j = 4, 0, 7

		board[ki, j].piece = king
		board[ri, j].piece = rook

		#Preconditions:
		self.assertTrue(board[ki, j].piece)
		self.assertTrue(board[ri, j].piece)
		self.assertTrue(not board[ki-1, j].piece)
		self.assertTrue(not board[ki-2, j].piece)

		#Perform castling:
		move = Castling("left", board.white)
		move.perform(board)

		#Postconditions after castling
		self.assertTrue(not board[ki, j].piece)
		self.assertTrue(not board[ri, j].piece)
		self.assertTrue(board[ki-1, j].piece)
		self.assertTrue(board[ki-2, j].piece)

		#Undo castling:
		move.undo(board)

		#Undo postconditions:
		self.assertTrue(board[ki, j].piece)
		self.assertTrue(board[ri, j].piece)
		self.assertTrue(not board[ki-1, j].piece)
		self.assertTrue(not board[ki-2, j].piece)

	def test_castling_white_right(self):
		'''Test performing a castling move to the right and then undoing it.'''
		board = Board(10, 10)
		board.current_turn = board.white
		king = King(board.white)
		rook = Rook(board.white)

		ki, ri, j = 4, 7, 7

		board[ki, j].piece = king
		board[ri, j].piece = rook

		#Preconditions:
		self.assertTrue(board[ki, j].piece)
		self.assertTrue(board[ri, j].piece)
		self.assertTrue(not board[ki+1, j].piece)
		self.assertTrue(not board[ki+2, j].piece)

		#Perform castling:
		move = Castling("right", board.white)
		move.perform(board)

		#Postconditions after castling
		self.assertTrue(not board[ki, j].piece)
		self.assertTrue(not board[ri, j].piece)
		self.assertTrue(board[ki+1, j].piece)
		self.assertTrue(board[ki+2, j].piece)

		#Undo castling:
		move.undo(board)

		#Undo postconditions:
		self.assertTrue(board[ki, j].piece)
		self.assertTrue(board[ri, j].piece)
		self.assertTrue(not board[ki+1, j].piece)
		self.assertTrue(not board[ki+2, j].piece)

	def test_crowning_perform_undo(self):
		'''Test performing a crowning move and then undoing it'''
		#init:
		board = Board(10, 10)
		pawn = Pawn(board.white)

		i, j = 0, 1
		board[i, j].piece = pawn
		src_type = str(pawn).split(" ")[0].replace("<", "")

		move = filter(lambda x: x.type == "Crowning", pawn.get_moves((i, j), board))[0]

		#Preconditions:
		self.assertTrue(not board[i, j-1].piece)
		self.assertTrue(board[i, j].piece)

		move.perform(board)

		self.assertTrue(board[i, j-1].piece)
		self.assertTrue(not board[i, j].piece)
		self.assertTrue(move.performed)

		#compare piece types (should differ if crowning succeeded):
		dst_type = str(board[i, j-1].piece).split(" ")[0].replace("<","")
		self.assertTrue(src_type != dst_type)

		#undo move:
		move.undo(board)
		self.assertTrue(not board[i, j-1].piece)
		self.assertTrue(board[i, j].piece)
		self.assertTrue(not move.performed)

		#compare piece types (should be both pawns):
		dst_type = str(board[i, j].piece).split(" ")[0].replace("<","")
		self.assertTrue(src_type == dst_type)

if __name__ == "__main__":
	unittest.main()
