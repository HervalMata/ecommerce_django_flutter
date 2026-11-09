import 'package:equatable/equatable.dart';

enum AddressType { home, work, other }

class Address extends Equatable {
  final String id;
  final AddressType addressType;
  final String fullName;
  final String phone;
  final String streetAddress;
  final String city;
  final String? district;
  final String? postalCode;
  final String country;
  final bool isDefault;
  final DateTime createdAt;
  final DateTime updatedAt;

  const Address({
    required this.id,
    required this.addressType,
    required this.fullName,
    required this.phone,
    required this.streetAddress,
    required this.city,
    this.district,
    this.postalCode,
    required this.country,
    required this.isDefault,
    required this.createdAt,
    required this.updatedAt
  });

  @override
  List<Object?> get props => [
    id,
    addressType,
    fullName,
    phone,
    streetAddress,
    city,
    district,
    postalCode,
    country,
    isDefault,
    createdAt,
    updatedAt,
  ];
}