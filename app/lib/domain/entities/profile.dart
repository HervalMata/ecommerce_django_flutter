import 'package:app/domain/entities/user.dart';
import 'package:equatable/equatable.dart';

enum Gender { female, male, other }

enum PreferredSize { xs, s, m, l, xl, xxl }

class Profile extends Equatable {
  final User user;
  final String? avatarUrl;
  final String? name;
  final Gender? gender;
  final PreferredSize? preferredSize;
  final Map<String, dynamic> stylePreferences;
  final double? heightCm;
  final double? weightKg;
  final String sizeSystem;
  final String currency;
  final String language;
  final String country;
  final DateTime createdAt;
  final DateTime updatedAt;

  const Profile({
    required this.user,
    required this.avatarUrl,
    required this.name,
    required this.gender,
    required this.preferredSize,
    this.stylePreferences = const {},
    required this.heightCm,
    required this.weightKg,
    this.sizeSystem = 'US',
    this.currency = 'BRL',
    this.language = 'pt-BR',
    this.country = 'Brasil',
    required this.createdAt,
    required this.updatedAt
  });

  @override
  List<Object?> get props => [
    user,
    avatarUrl,
    name,
    gender,
    preferredSize,
    stylePreferences,
    heightCm,
    weightKg,
    sizeSystem,
    currency,
    language,
    country,
    createdAt,
    updatedAt,
  ];
}