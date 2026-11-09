import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String email;
  final String? phone;
  final DateTime dateJoined;

  const User({
    required this.id,
    required this.email,
    this.phone,
    required this.dateJoined
  });

  @override
  List<Object?> get props => [id, email, phone, dateJoined];
}