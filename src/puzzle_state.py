from dataclasses import dataclass
from typing import List

# represents single cell in the shipping container grid
@dataclass
class Cell:
      exists: bool # False = NAN (no slot available)
      weight: int # 0 = UNUSED or empty container
      description: str # empty string when UNUSED or NAN

@dataclass
class PuzzleState:
      grid: List[List[Cell]]

      # initialize empty grid with all cells as NAN
      @staticmethod
      def create_empty(rows: int = 8, cols: int = 12) -> 'PuzzleState': # default size 8 x 12 to specifications
            # expression to create ROWS of cells, then COLS of those rows
            return PuzzleState(grid=[
                  [Cell(exists=False, weight=0, description="") for _ in range(cols)]
                  for _ in range(rows)
            ])


      @classmethod
      def generate_state_from_manifest_data(cls, manifest_data: List[tuple[int, int, int, str]]) -> 'PuzzleState':
            state = cls.create_empty()

            for row, col, weight, desc in manifest_data:
                  if desc == "NAN":
                        state.grid[row][col] = Cell(exists = False, weight = 0, description=desc)
                  elif desc == "UNUSED":
                        state.grid[row][col] = Cell(exists = True, weight = 0, description=desc)
                  else:
                        state.grid[row][col] = Cell(exists = True, weight = weight, description=desc)


            return state