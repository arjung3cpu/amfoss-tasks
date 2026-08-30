import 'dart:async';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(const OnePieceMemoryApp());
}

class OnePieceMemoryApp extends StatefulWidget {
  const OnePieceMemoryApp({super.key});

  @override
  State<OnePieceMemoryApp> createState() => _OnePieceMemoryAppState();
}

class _OnePieceMemoryAppState extends State<OnePieceMemoryApp> {
  ThemeMode _themeMode = ThemeMode.dark;

  @override
  void initState() {
    super.initState();
    _loadTheme();
  }

  Future<void> _loadTheme() async {
    final prefs = await SharedPreferences.getInstance();
    final isDark = prefs.getBool('darkMode') ?? true;

    setState(() {
      _themeMode = isDark ? ThemeMode.dark : ThemeMode.light;
    });
  }

  Future<void> _toggleTheme() async {
    final isDark = _themeMode == ThemeMode.dark;

    setState(() {
      _themeMode = isDark
          ? ThemeMode.light
          : ThemeMode.dark;
    });

    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(
      'darkMode',
      _themeMode == ThemeMode.dark,
    );
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'One Piece Memory Matcher',
      themeMode: _themeMode,
      theme: ThemeData(
        brightness: Brightness.light,
        colorSchemeSeed: Colors.red,
        useMaterial3: true,
      ),
      darkTheme: ThemeData(
        brightness: Brightness.dark,
        colorSchemeSeed: Colors.red,
        scaffoldBackgroundColor: const Color(0xFF090909),
        useMaterial3: true,
      ),
      home: MemoryGame(
        onToggleTheme: _toggleTheme,
        isDark: _themeMode == ThemeMode.dark,
      ),
    );
  }
}

class MemoryCard {
  final String name;
  final String emoji;
  bool isFaceUp;
  bool isMatched;

  MemoryCard({
    required this.name,
    required this.emoji,
    this.isFaceUp = false,
    this.isMatched = false,
  });
}

class MemoryGame extends StatefulWidget {
  final VoidCallback onToggleTheme;
  final bool isDark;

  const MemoryGame({
    super.key,
    required this.onToggleTheme,
    required this.isDark,
  });

  @override
  State<MemoryGame> createState() => _MemoryGameState();
}

class _MemoryGameState extends State<MemoryGame> {
  final Random _random = Random();

  final List<Map<String, String>> _characters = [
    {'name': 'Luffy', 'emoji': '🏴‍☠️'},
    {'name': 'Zoro', 'emoji': '⚔️'},
    {'name': 'Nami', 'emoji': '🍊'},
    {'name': 'Sanji', 'emoji': '🔥'},
    {'name': 'Usopp', 'emoji': '🎯'},
    {'name': 'Chopper', 'emoji': '🦌'},
    {'name': 'Robin', 'emoji': '🌸'},
    {'name': 'Franky', 'emoji': '🤖'},
  ];

  List<MemoryCard> _cards = [];

  int _firstIndex = -1;
  int _secondIndex = -1;

  int _moves = 0;
  int _score = 0;
  int _seconds = 0;
  int _bestScore = 0;

  bool _busy = false;
  bool _gameWon = false;

  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _loadBestScore();
    _startNewGame();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  Future<void> _loadBestScore() async {
    final prefs = await SharedPreferences.getInstance();

    setState(() {
      _bestScore = prefs.getInt('bestScore') ?? 0;
    });
  }

  Future<void> _saveBestScore() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('bestScore', _bestScore);
  }

  void _startTimer() {
    _timer?.cancel();

    _timer = Timer.periodic(
      const Duration(seconds: 1),
      (_) {
        if (!_gameWon) {
          setState(() {
            _seconds++;
          });
        }
      },
    );
  }

  void _startNewGame() {
    _timer?.cancel();

    final newCards = <MemoryCard>[];

    for (final character in _characters) {
      newCards.add(
        MemoryCard(
          name: character['name']!,
          emoji: character['emoji']!,
        ),
      );

      newCards.add(
        MemoryCard(
          name: character['name']!,
          emoji: character['emoji']!,
        ),
      );
    }

    newCards.shuffle(_random);

    setState(() {
      _cards = newCards;
      _firstIndex = -1;
      _secondIndex = -1;
      _moves = 0;
      _score = 0;
      _seconds = 0;
      _busy = false;
      _gameWon = false;
    });

    _startTimer();
  }

  void _flipCard(int index) {
    if (_busy ||
        _cards[index].isFaceUp ||
        _cards[index].isMatched) {
      return;
    }

    setState(() {
      _cards[index].isFaceUp = true;
    });

    if (_firstIndex == -1) {
      _firstIndex = index;
      return;
    }

    _secondIndex = index;

    setState(() {
      _moves++;
      _busy = true;
    });

    _checkMatch();
  }

  Future<void> _checkMatch() async {
    await Future.delayed(
      const Duration(milliseconds: 700),
    );

    final first = _cards[_firstIndex];
    final second = _cards[_secondIndex];

    if (first.name == second.name) {
      setState(() {
        first.isMatched = true;
        second.isMatched = true;

        _score += 100;

        _busy = false;
        _firstIndex = -1;
        _secondIndex = -1;
      });

      _checkWin();
    } else {
      setState(() {
        first.isFaceUp = false;
        second.isFaceUp = false;

        _busy = false;
        _firstIndex = -1;
        _secondIndex = -1;
      });
    }
  }

  void _checkWin() {
    final allMatched =
        _cards.every((card) => card.isMatched);

    if (!allMatched) {
      return;
    }

    _timer?.cancel();

    final finalScore =
        max(0, _score - (_moves * 5) - (_seconds ~/ 2));

    setState(() {
      _score = finalScore;
      _gameWon = true;
    });

    if (_bestScore == 0 ||
        finalScore > _bestScore) {
      setState(() {
        _bestScore = finalScore;
      });

      _saveBestScore();

      _showWinDialog(
        isNewBest: true,
      );
    } else {
      _showWinDialog(
        isNewBest: false,
      );
    }
  }

  void _showWinDialog({
    required bool isNewBest,
  }) {
    Future.delayed(
      const Duration(milliseconds: 300),
      () {
        if (!mounted) return;

        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (context) {
            return AlertDialog(
              title: Text(
                isNewBest
                    ? '🏆 New Best Score!'
                    : '🎉 Grand Line Complete!',
              ),
              content: Text(
                'Score: $_score\n'
                'Moves: $_moves\n'
                'Time: ${_formatTime(_seconds)}',
              ),
              actions: [
                TextButton(
                  onPressed: () {
                    Navigator.pop(context);
                    _startNewGame();
                  },
                  child: const Text(
                    'PLAY AGAIN',
                  ),
                ),
              ],
            );
          },
        );
      },
    );
  }

  String _formatTime(int seconds) {
    final minutes = seconds ~/ 60;
    final remainingSeconds = seconds % 60;

    return '${minutes.toString().padLeft(2, '0')}:'
        '${remainingSeconds.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'ONE PIECE MEMORY MATCHER',
          style: TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
        actions: [
          IconButton(
            tooltip: 'Toggle theme',
            onPressed: widget.onToggleTheme,
            icon: Icon(
              widget.isDark
                  ? Icons.light_mode
                  : Icons.dark_mode,
            ),
          ),
          IconButton(
            tooltip: 'New game',
            onPressed: _startNewGame,
            icon: const Icon(
              Icons.refresh,
            ),
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            _buildHeader(theme),
            Expanded(
              child: _buildGameGrid(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(ThemeData theme) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(
        16,
        16,
        16,
        10,
      ),
      child: Column(
        children: [
          Text(
            '🏴‍☠️ FIND THE CREW',
            style: theme.textTheme.headlineSmall
                ?.copyWith(
              fontWeight: FontWeight.w900,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'Match every pair and become the King of Memory!',
            textAlign: TextAlign.center,
            style: theme.textTheme.bodyMedium,
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              _StatCard(
                icon: Icons.stars,
                label: 'SCORE',
                value: '$_score',
              ),
              const SizedBox(width: 8),
              _StatCard(
                icon: Icons.touch_app,
                label: 'MOVES',
                value: '$_moves',
              ),
              const SizedBox(width: 8),
              _StatCard(
                icon: Icons.timer,
                label: 'TIME',
                value: _formatTime(_seconds),
              ),
              const SizedBox(width: 8),
              _StatCard(
                icon: Icons.emoji_events,
                label: 'BEST',
                value: '$_bestScore',
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildGameGrid() {
    return LayoutBuilder(
      builder: (context, constraints) {
        final width = constraints.maxWidth;

        int columns;

        if (width < 400) {
          columns = 3;
        } else if (width < 700) {
          columns = 4;
        } else {
          columns = 6;
        }

        return GridView.builder(
          padding: const EdgeInsets.all(16),
          gridDelegate:
              SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: columns,
            crossAxisSpacing: 10,
            mainAxisSpacing: 10,
            childAspectRatio: 0.82,
          ),
          itemCount: _cards.length,
          itemBuilder: (context, index) {
            return _MemoryCardWidget(
              card: _cards[index],
              onTap: () => _flipCard(index),
            );
          },
        );
      },
    );
  }
}

class _StatCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _StatCard({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Card(
        child: Padding(
          padding: const EdgeInsets.symmetric(
            vertical: 10,
            horizontal: 4,
          ),
          child: Column(
            children: [
              Icon(
                icon,
                size: 20,
              ),
              const SizedBox(height: 4),
              Text(
                label,
                style: const TextStyle(
                  fontSize: 9,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Text(
                value,
                style: const TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w900,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _MemoryCardWidget extends StatelessWidget {
  final MemoryCard card;
  final VoidCallback onTap;

  const _MemoryCardWidget({
    required this.card,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    final revealed =
        card.isFaceUp || card.isMatched;

    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(
          milliseconds: 250,
        ),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(14),
          color: revealed
              ? theme.colorScheme.surface
              : theme.colorScheme.primary,
          border: Border.all(
            color: card.isMatched
                ? Colors.green
                : theme.colorScheme.outline,
            width: card.isMatched ? 3 : 1,
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.25),
              blurRadius: 5,
              offset: const Offset(0, 3),
            ),
          ],
        ),
        child: Center(
          child: revealed
              ? Column(
                  mainAxisAlignment:
                      MainAxisAlignment.center,
                  children: [
                    Text(
                      card.emoji,
                      style: const TextStyle(
                        fontSize: 34,
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      card.name,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 12,
                      ),
                    ),
                    if (card.isMatched)
                      const Padding(
                        padding: EdgeInsets.only(
                          top: 5,
                        ),
                        child: Icon(
                          Icons.check_circle,
                          color: Colors.green,
                          size: 18,
                        ),
                      ),
                  ],
                )
              : Column(
                  mainAxisAlignment:
                      MainAxisAlignment.center,
                  children: [
                    const Text(
                      '☠️',
                      style: TextStyle(
                        fontSize: 32,
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      'GRAND\nLINE',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.white
                            .withOpacity(0.9),
                        fontWeight: FontWeight.w900,
                        fontSize: 10,
                        letterSpacing: 1,
                      ),
                    ),
                  ],
                ),
        ),
      ),
    );
  }
}