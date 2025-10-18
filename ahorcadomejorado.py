#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Juego: El Ahorcado (versión mejorada)
Autor: Cristian Clerque
Descripción:
Versión mejorada del clásico "Ahorcado" con sistema de puntuación, dificultad,
pistas, historial y estadísticas.
"""

import random
import os
import string
from typing import List, Set

# --- Palabras por defecto ---
DEFAULT_WORDS = [
    "python", "programacion", "computadora", "variable", "funcion",
    "algoritmo", "desarrollo", "inteligencia", "estructura", "condicional",
    "bucle", "recursion", "modulo", "clase", "objeto", "debugging"
]

HANGMAN_STAGES = [
    """
     _______
    |/      |
    |
    |
    |
    |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |
    |
    |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |       |
    |       |
    |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |      \\|
    |       |
    |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |      \\|/
    |       |
    |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |      \\|/
    |       |
    |      /
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |      \\|/
    |       |
    |      / \\
    |
    |___
    """
]

# --- Funciones auxiliares ---

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def load_words(filename="words.txt") -> List[str]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [w.strip().lower() for w in f if w.strip()]
    except FileNotFoundError:
        return DEFAULT_WORDS

def save_score(score: int):
    with open("score.txt", "a", encoding="utf-8") as f:
        f.write(str(score) + "\n")

def get_best_score() -> int:
    try:
        with open("score.txt", "r", encoding="utf-8") as f:
            scores = [int(x) for x in f.read().split()]
            return max(scores) if scores else 0
    except FileNotFoundError:
        return 0

def record_history(result: str, word: str, score: int):
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(f"Resultado: {result} | Palabra: {word} | Puntos: {score}\n")

def get_stats():
    try:
        with open("history.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            wins = sum(1 for l in lines if "Ganaste" in l)
            losses = sum(1 for l in lines if "Perdiste" in l)
            return wins, losses
    except FileNotFoundError:
        return 0, 0

def choose_word(words, difficulty: str) -> str:
    if difficulty == "1":
        filtered = [w for w in words if len(w) <= 5]
    elif difficulty == "2":
        filtered = [w for w in words if 6 <= len(w) <= 8]
    else:
        filtered = [w for w in words if len(w) > 8]
    return random.choice(filtered) if filtered else random.choice(words)

def display_state(secret, guessed, errors, max_errors, score):
    print(HANGMAN_STAGES[min(errors, len(HANGMAN_STAGES)-1)])
    print("Palabra: ", " ".join([ch if ch in guessed else "_" for ch in secret]))
    print(f"Letras: {' '.join(sorted(guessed)) or '---'}")
    print(f"Errores: {errors}/{max_errors}")
    print(f"Puntuación: {score}")

# --- Juego principal ---

def play_game(words):
    clear_screen()
    print("Selecciona dificultad:")
    print("1) Fácil   (más intentos)")
    print("2) Media   (equilibrado)")
    print("3) Difícil (menos intentos)")
    difficulty = input("Elige (1-3): ").strip()
    max_errors = 8 if difficulty == "1" else 6 if difficulty == "2" else 4

    secret = choose_word(words, difficulty)
    guessed = set()
    errors = 0
    score = 0
    hint_used = False

    while True:
        clear_screen()
        display_state(secret, guessed, errors, max_errors, score)

        if set(secret).issubset(guessed):
            print(f"\n¡Ganaste! La palabra era '{secret}'.")
            bonus = (max_errors - errors) * 2
            score += bonus
            print(f"Bonificación: +{bonus} puntos")
            save_score(score)
            record_history("Ganaste", secret, score)
            break

        if errors >= max_errors:
            print(f"\nPerdiste. La palabra era '{secret}'.")
            record_history("Perdiste", secret, score)
            break

        print("\nOpciones: letra / *pista / *salir")
        guess = input("→ ").strip().lower()

        if guess == "*salir":
            print("Saliendo de la partida...")
            break
        elif guess == "*pista" and not hint_used:
            letters_left = [c for c in secret if c not in guessed]
            if letters_left:
                hint = random.choice(letters_left)
                guessed.add(hint)
                hint_used = True
                score -= 2
                print(f"Pista: La palabra contiene la letra '{hint}'. (-2 puntos)")
                input("Presiona Enter...")
            continue
        elif len(guess) != 1 or guess not in string.ascii_lowercase:
            print("Entrada inválida.")
            input("Presiona Enter...")
            continue
        elif guess in guessed:
            print("Ya probaste esa letra.")
            input("Presiona Enter...")
            continue

        guessed.add(guess)
        if guess in secret:
            print(f"¡Bien hecho! '{guess}' está en la palabra.")
            score += 1
        else:
            print(f"Error. '{guess}' no está en la palabra.")
            errors += 1
        input("Presiona Enter...")

# --- Menú principal ---

def main():
    words = load_words()
    while True:
        clear_screen()
        best = get_best_score()
        wins, losses = get_stats()

        print("=== JUEGO DEL AHORCADO ===")
        print("1) Jugar")
        print("2) Ver mejores puntuaciones")
        print("3) Ver estadísticas")
        print("4) Salir")
        print("---------------------------")
        print(f"Mejor puntuación: {best}")
        print(f"Victorias: {wins} | Derrotas: {losses}")
        choice = input("Elige una opción: ").strip()

        if choice == "1":
            play_game(words)
        elif choice == "2":
            clear_screen()
            print(f"Tu mejor puntuación es: {best} puntos.")
            input("Presiona Enter para volver...")
        elif choice == "3":
            clear_screen()
            print(f"Has ganado {wins} partidas y perdido {losses}.")
            input("Presiona Enter para volver...")
        elif choice == "4":
            print("¡Hasta luego!")
            break
        else:
            input("Opción inválida. Presiona Enter...")

if __name__ == "__main__":
    main()
