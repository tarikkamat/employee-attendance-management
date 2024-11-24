from django.db import models


class AttendancesTypes(models.TextChoices):
    LOGIN = 'LOGIN', 'Oturum Başlatma'
    LOGOUT = 'LOGOUT', 'Oturum Sonlandırma'


class LeaveReasonTypes(models.TextChoices):
    ANNUAL = 'ANNUAL', 'Yıllık İzin'
    RELOCATION = 'RELOCATION', 'Taşınma İzni'
    SICK = 'SICK', 'Hastalık İzni'
    DEATH_OF_CHILD_OR_SPOUSE = 'DEATH_OF_CHILD_OR_SPOUSE', 'Çocuk veya Eşin Vefatı'
    DEATH_OF_MOM_DAD_OR_SIBLING = 'DEATH_OF_MOM_DAD_OR_SIBLING', 'Anne, Baba veya Kardeşin Vefatı'
    DEATH_OF_SPOUSE_MOM_DAD_SIBLING = 'DEATH_OF_SPOUSE_MOM_DAD_SIBLING', 'Eş, Anne, Baba veya Kardeşin Vefatı'
    BIRTH_DAY = 'BIRTH_DAY', 'Doğum Günü İzni'
    SPOUSE_BIRTH_DAY = 'SPOUSE_BIRTH_DAY', 'Eşin Doğum Günü İzni'
    COMPASSIONATE_LEAVE = 'COMPASSIONATE_LEAVE', 'Mazaret İzni'
    MILITARY_LEAVE = 'MILITARY_LEAVE', 'Askerlik İzni'
    MATERNITY_LEAVE = 'MATERNITY_LEAVE', 'Süt İzni'
    FREE_LEAVE = 'FREE_LEAVE', 'Ücretsiz İzin'
    MARRIAGE_LEAVE = 'MARRIAGE_LEAVE', 'Düğün İzni'


class LeaveStatusTypes(models.TextChoices):
    PENDING = 'PENDING', 'Onay Bekliyor'
    APPROVED = 'APPROVED', 'Onaylandı'
    REJECTED = 'REJECTED', 'Reddedildi'
