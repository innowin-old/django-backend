from graphene import AbstractType

from users.schemas.mutations.skill import CreateSkillMutation,\
    UpdateSkillMutation, DeleteSkillMutation
from users.schemas.mutations.work_experience import CreateWorkExperienceMutation,\
    UpdateWorkExperienceMutation, DeleteWorkExperienceMutation,\
    ConfirmWorkExperienceMutation
from users.schemas.mutations.certificate import CreateCertificateMutation,\
    UpdateCertificateMutation, DeleteCertificateMutation
from users.schemas.mutations.research import CreateResearchMutation,\
    UpdateResearchMutation, DeleteResearchMutation
from users.schemas.mutations.education import CreateEducationMutation,\
    UpdateEducationMutation, DeleteEducationMutation
from users.schemas.mutations.user import RegisterUserMutation,\
    ChangePasswordMutation, PasswordResetMutation, UpdateProfileMutation


class UserMutation(AbstractType):
    # ---------------- Skill ----------------
    create_skill = CreateSkillMutation.Field()
    update_skill = UpdateSkillMutation.Field()
    delete_skill = DeleteSkillMutation.Field()

    # ---------------- Work Experience ----------------
    create_work_experience = CreateWorkExperienceMutation.Field()
    update_work_experience = UpdateWorkExperienceMutation.Field()
    delete_work_experience = DeleteWorkExperienceMutation.Field()
    confirm_work_experience = ConfirmWorkExperienceMutation.Field()

    # ---------------- Certificate ----------------
    create_certificate = CreateCertificateMutation.Field()
    update_certificate = UpdateCertificateMutation.Field()
    delete_certificate = DeleteCertificateMutation.Field()

    # ---------------- Research ----------------
    create_research = CreateResearchMutation.Field()
    update_research = UpdateResearchMutation.Field()
    delete_research = DeleteResearchMutation.Field()

    # ---------------- Education ----------------
    create_education = CreateEducationMutation.Field()
    update_education = UpdateEducationMutation.Field()
    delete_education = DeleteEducationMutation.Field()

    # ---------------- Profile ----------------
    update_profile = UpdateProfileMutation.Field()

    # ---------------- User ----------------
    register_user = RegisterUserMutation.Field()
    change_password = ChangePasswordMutation.Field()
    password_reset = PasswordResetMutation.Field()
