import cvision
import solver

def main():
    extractor = cvision.Puzzle("../imgs/puzzle.png")
    extractor.load_image()
    extractor.detect_lines()
    extractor.detect_numbers()

    puzzle = solver.Solver(extractor.parsed_board)
    print(puzzle)
    puzzle.solve_sudoku()
    print(puzzle)

if __name__ == '__main__':
    main()