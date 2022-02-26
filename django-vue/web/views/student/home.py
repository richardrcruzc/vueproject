from django.shortcuts import get_object_or_404, render
from ..base import ProtectedView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from ...models.student import StudentProfile, StudentReport, ReportDetail

from arc.settings.base import BASE_DIR

# -----------------change--------------------
from ...models.test import final_test_state
# --------------------end---------------------
import os

BASIC_READING = [
    '1-di-tepi-kolam.jpg',
    '2-hujan.jpg',
    '3-sarang-burung.jpg',
    '4-lari.jpg',
    '5-gajah.jpg',
    '6-tolong.jpg',
    '7-jangan-belang.jpg',
    '8-bendera-singapura.jpg',
    '9-haiwan.jpg',
    '10-pasar-raya.jpg',
    '11-tanam-pokok.jpg',
    '12-pelihara-ikan.jpg',
    '13-di-tepi-kolam-2.jpg',
    '14-di-taman.jpg',
    '15-padang-sekolah.jpg',
    '16-bola-sepak.jpg',
    '17-kawan-baik-saya.jpg',
    '18-naik-bas.jpg',
    '19-taman-merlion.jpg',
    '20-pemotong-kayu.jpg',
    '21-jiran-adi.jpg',
    '22-putih-dan-kelabu.jpg',
    '23-kuda-mainan.jpg',
    '24-kasihan.jpg',
    '25-di-mana-didi.jpg',
    '26-lela-jatuh.jpg',
    '27-membaca.jpg',
    '28-arnab-dengan-kura-kura.jpg',
    '29-cuti-sekolah.jpg',
    '30-manis.jpg',
    '31-pancing-ikan.jpg',
    '32-taman-bunga.jpg',
    '33-bunga-besar.jpg',
    '34-sampan-kertas.jpg',
    '35-ibu-sakit.jpg',
    '36-pimpin-tangan.jpg',
    '37-mandi-di-sungai.jpg',
    '38-keluarga-itik.jpg',
    '39-didi-sedih.jpg',
    '40-ikan-comel.jpg',
    '41-semut-rajin.jpg',
    '42-pulang-sekolah.jpg',
    '43-susu-lembu.jpg',
    '44-surat.jpg',
    '45-kad-hari-guru.jpg',
    '46-pokok-krismas.jpg',
    '47-musim-sejuk.jpg',
    '48-anak-patung.jpg',
    '49-rajin-membaca.jpg',
    '50-tanglung.jpg',
    '51-sama-sama-cantik.jpg',
    '52-masuk-kampung.jpg',
    '53-kicau-burung.jpg',
    '54-latih-sukan.jpg',
    '55-belajar.jpg',
    '56-belang.jpg',
    '57-jangan-makan-saya.jpg',
    '58-adik-comel.jpg',
    '59-adik-pandai.jpg',
    '60-merlion.jpg',
    '61-di-tepi-pantai.jpg',
    '62-monyet-dengan-kura-kura.jpg',
    '63-kawan-datuk.jpg',
    '64-polis-dan-pencuri.jpg',
    '65-sarang-semut.jpg',
    '66-minum-apa.jpg',
    '67-keluarga-saya.jpg',
    '68-sayang-nenek.jpg',
    '69-semut-merah.jpg',
    '70-kuda-kayu.jpg',
    '71-rak-buku.jpg',
    '72-ke-tadika.jpg',
    '73-buat-apa.jpg',
    '74-pelangi.jpg',
    '75-anak-patung-baharu.jpg',
    '76-menolong-ibu.jpg',
    '77-cerita-saya.jpg',
    '78-kucing-dengan-tikus.jpg',
    '79-cuti-sekolah.jpg',
    '80-kasur-baharu.jpg',
    '81-main-sembunyi-sembunyi.jpg',
    '82-terima-kasih-alif.jpg',
    '83-lumba-lari.jpg',
    '84-sepasang-burung.jpg',
    '85-estet-perumahan.jpg',
    '86-salah-siapa.jpg',
    '87-hutan-terbakar.jpg',
    '88-mencari-makanan.jpg',
    '89-bintang-kecil.jpg',
    '90-kumbang-mencari-bunga.jpg',
    '91-ani-rajin.jpg',
    '92-bendera-negara-kita.jpg',
    '93-kereta-bamper.jpg',
    '94-sarkis.jpg',
    '95-mari-makan.jpg',
    '96-warna-payung.jpg',
    '97-beca.jpg',
    '98-amboi-cantiknya.jpg',
    '99-sama-sama-rugi.jpg',
    '100-sarapan-saya.jpg',
    '101-sekolah-baharu.jpg',
    '102-tempat-tempat-di-sekolah-saya.jpg',
    '103-tekun-belajar-seronok-bermain.jpg',
    '104-sekolah-saya-indah.jpg',
    '105-ayu-murid-darjah-satu.jpg',
    '106-siap-ke-sekolah.jpg',
    '107-membaca-dan-menulis.jpg',
    '108-menghantar-surat.jpg',
    '109-hani-pandai-melukis.jpg',
    '110-belajar-menyanyi.jpg',
    '111-belajar-mengira.jpg',
    '112-sani-gemar-melukis.jpg',
    '113-cantik-lukisan-nina.jpg',
    '114-rintik-rintik-hujan.jpg',
    '115-menolong-ibu.jpg',
    '116-kad-hari-lahir.jpg',
    '117-di-tepi-pantai.jpg',
    '118-kita-warga-singapura.jpg',
    '119-mencari-madu-bunga.jpg',
    '120-bendera-negara.jpg',
    '121-buah-belimbing.jpg',
    '122-cita-cita-saya.jpg',
    '123-kemas-dan-rapi.jpg',
    '124-negara-singapura.jpg',
    '125-memberus-gigi.jpg',
]

class StudentView(ProtectedView):
    def get(self, request):
        self.context.update({'page_title': ' '})
        student_profile = StudentProfile.objects.filter(student=request.user).first()
        is_act = False
        is_new = True
        if student_profile:
            is_new = student_profile.is_new
        else:
            student_profile = StudentProfile()
            student_profile.student = request.user
            student_profile.save()

        if student_profile.change_password:
            return HttpResponseRedirect('/update-password/')

        has_avatar = True if student_profile.avatar is not None else False

        if not has_avatar:
            return redirect('/avatar')
        if is_new:
            return redirect('/quiz/start')
        else:
            # change the ---------------------------ftf---------------
            final_test_check = final_test_state.objects.order_by('-created').first()
            print(final_test_check.state)
            # --------------------end---------------------
            basic_readings = []
            # change the ---------------------------ftf---------------
            total_finish_test = 0
            total_tests = StudentReport.objects.filter(student=request.user).all()
            for total_test in total_tests:
                num_correct = ReportDetail.objects.filter(student_report_id=total_test.id, is_correct=1).count()
                if num_correct is 4:
                    total_finish_test = total_finish_test + 1
            trophy = (int)((total_finish_test - total_finish_test % 3)/3)
            star = total_finish_test % 3
            print(trophy)
            total_result = {
                'trophy': trophy,
                'star': star,
            }

            readings_dir = os.path.join(os.path.join(BASE_DIR, 'static'), 'bacaan-asas')

            for reading in BASIC_READING:
                reading_title = ' '.join(reading[:-4].split('-')[1:]).title()

                basic_readings.append({
                    'title': reading_title,
                    'url': '/static/bacaan-asas/' + reading
                })
            self.context.update({'final_test_act': final_test_check.state})
            self.context.update({'total_result': total_result})
            self.context.update({'avatar': 'start-quiz_' + str(student_profile.avatar+1) + '.png'})
            self.context.update({'basic_readings': basic_readings})
            return self.render(request, 'arc/student/dashboard.html')


class AvatarView(ProtectedView):
    def get(self, request):
        self.context.update({'page_title': ' '})

        try:
            avatar_selection = int(request.GET.get('selection', -1))
            if avatar_selection < 0 or avatar_selection > 11:
                avatar_selection = -1
        except:
            avatar_selection = -1

        student_profile = StudentProfile.objects.filter(student=request.user).first()

        has_avatar = False
        if student_profile:
            has_avatar = True if student_profile.avatar is not None else False
            if not has_avatar and avatar_selection != -1:
                student_profile.avatar = avatar_selection
                student_profile.save()
                has_avatar = True
        else:
            student_profile = StudentProfile()
            student_profile.student = request.user
            student_profile.save()

        if has_avatar:
            return redirect('/')
        else:
            avatars = []
            for i in range(12):
                avatars.append({
                    'id': i,
                    'file': 'avatar_' + str(i+1) + '.jpg'
                })
            self.context.update({'avatars': avatars})
            self.context.update({'page_main_menu_empty': True})
            return self.render(request, 'arc/student/avatar.html')
