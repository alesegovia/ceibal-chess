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

from board import Board
from piece import Move, Pawn, King, Queen
from errors import MoveError

class BoardTest(unittest.TestCase):
	'''Perform unit testing on the new Board class.'''

	def test_king_is_checked(self):
		board = Board()
		board[0, 0].piece = King(board.black)
		board[1, 1].piece = Queen(board.white)
		board[7, 7].piece = King(board.white)
		self.assertTrue(board.king_is_checked(board.black))
		self.assertFalse(board.king_is_checked(board.white))

	def test_king_is_checkmated(self):
		board = Board()
		board[0, 0].piece = King(board.black)
		board[1, 1].piece = Queen(board.white)
		board[7, 7].piece = King(board.white)
		self.assertFalse(board.king_is_checkmated(board.black))

		board[2, 2].piece = Queen(board.white)
		self.assertTrue(board.king_is_checkmated(board.black))

	def test_board_creation(self):
		'''Test creating a board.

		'''

		board = Board()

		self.assertTrue(len(board.board) == 8)
		self.assertTrue(len(board.board[c]) == 8 for c in range(0,8))

	def test_move_piece_in_cell_to_dest(self):
		'''Test moving a piece in a selected cell to a given destination.

		This method evaluates performing moves on the board in the same way the
		BoardController class does.

		'''

		#Setup board with a white pawn at start position (1,6)
		board = Board()
		pawn = Pawn(board.white)

		board[0, 4].piece = King(board.black)
		board[7, 4].piece = King(board.white)

		col, row = 1, 6

		board[col, row].piece = pawn

		#Simulate BoardController:
		selected_cell = board[col, row]
		#board.on_cell_selected(selected_cell)

		#Preconditions:
		self.assertTrue(board.can_move_piece_in_cell_to(selected_cell,
												  (col, row-1)))
		self.assertTrue(board.can_move_piece_in_cell_to(selected_cell,
												  (col, row-2)))

		#Check whether cells are aware of the moves that take pieces to them
		#self.assertTrue(len(board[col, row-1].moves) == 1)
		#self.assertTrue(len(board[col, row-2].moves) == 1)

		#Perform movement:
		board.move_piece_in_cell_to(pawn.owner, (col, row), (col, row-1))

		#Check whether cells have been clean
		self.assertTrue(len(board[col, row-1].moves) == 0)
		self.assertTrue(len(board[col, row-2].moves) == 0)

	def test_move_wrong_piece_to_dest(self):
		''''Test requesting moving a wrong piece to a destination cell.

		'''

		#Setup board with a two white pawns:
		board = Board()
		pawn1 = Pawn(board.white)
		pawn2 = Pawn(board.white)

		board[0, 4].piece = King(board.black)
		board[7, 4].piece = King(board.white)

		col1, col2, row = 1, 3, 5

		board[col1, row].piece = pawn1
		board[col2, row].piece = pawn2

		#Simulate BoardController:
		selected_cell = board[col1, row]
		#board.on_cell_selected(selected_cell)

		#Preconditions:
		self.assertTrue(board.can_move_piece_in_cell_to(selected_cell,
												  (col1, row-1)))

		#Try moving pawn2 to the destination for pawn1:
		self.assertFalse(board.can_move_piece_in_cell_to(board[col2,row],
												   (col1, row-1)))
		self.assertRaises(MoveError, board.move_piece_in_cell_to,
					pawn2.owner, (col2,row), (col1, row-1))

if __name__ == "__main__":
	unittest.main()

