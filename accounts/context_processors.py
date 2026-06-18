def user_profiles(request):
    if request.user.is_authenticated:
        return {
            "has_doctor_profile": request.user.has_doctor_profile,
            "has_patient_profile": request.user.has_patient_profile,
            "user_doctor_profile": request.user.safe_doctor_profile,
            "user_patient_profile": request.user.safe_patient_profile,
        }
    return {}
