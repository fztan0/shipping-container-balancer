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

      @staticmethod
      def create_empty(rows: int = 8, cols: int = 12) -> 'PuzzleState':
            return PuzzleState(
                  grid=[[Cell(exists=False, weight=0, description="") for _ in range(cols)]
                        for _ in range(rows)]
            )


      @classmethod
      def from_manifest_data(cls, manifest_data: List[tuple[int, int, int, str]]) -> 'PuzzleState':
            state = cls.create_empty()
            for row, col, weight, desc in manifest_data:
                  if 0 <= row < len(state.grid) and 0 <= col < len(state.grid[0]):
                        state.grid[row][col] = Cell(
                              exists=True,
                              weight=weight,
                              description=desc,
                        )

            return state