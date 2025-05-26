def is_safe(board, row, col):
    """
    بررسی می‌کند که آیا قرار دادن یک وزیر در board[row] = col امن است یا خیر.
    board لیستی است که ستون وزیر در هر سطر را نشان می‌دهد.
    این تابع برای سطر 'row' و ستون 'col' بررسی می‌کند با توجه به وزیرهای قرار گرفته در سطرهای قبلی.
    """
    for prev_row in range(row):
        prev_col = board[prev_row]
        if prev_col == col or \
           abs(prev_row - row) == abs(prev_col - col):
            return False
    return True

def count_attacking_pairs(solution):
    """
    تعداد جفت وزیرهای مهاجم را در یک راه‌حل معین محاسبه می‌کند.
    solution لیستی است که solution[row] = col.
    """
    n = len(solution)
    if n <= 1:
        return 0
    
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            # وزیر i در (i, solution[i])
            # وزیر j در (j, solution[j])
            if solution[i] == solution[j]:  # تداخل ستون
                attacks += 1
            elif abs(i - j) == abs(solution[i] - solution[j]):  # تداخل قطر
                attacks += 1
    return attacks