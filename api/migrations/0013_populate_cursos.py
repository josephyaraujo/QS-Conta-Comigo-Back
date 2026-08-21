from django.db import migrations, models


def populate_cursos(apps, schema_editor):
    Cursos = apps.get_model('api', 'Cursos')
    
    cursos_data = [
        # Técnico Integrado (Ensino Médio)
        ("administracao", "Administração"),
        ("controle_ambiental", "Controle Ambiental"),
        ("edificacoes", "Edificações"),
        ("eletrotecnica", "Eletrotécnica"),
        ("geologia", "Geologia"),
        ("informatica_internet", "Informática para Internet"),
        ("manutencao_suporte", "Manutenção e Suporte em Informática"),
        ("mecanica", "Mecânica"),
        ("mineracao", "Mineração"),

        # Técnico Subsequente
        ("controle_ambiental_sub", "Controle Ambiental (Subsequente)"),
        ("edificacoes_sub", "Edificações (Subsequente)"),
        ("eletrotecnica_sub", "Eletrotécnica (Subsequente)"),
        ("geologia_sub", "Geologia (Subsequente)"),
        ("mecanica_sub", "Mecânica (Subsequente)"),
        ("mineracao_sub", "Mineração (Subsequente)"),
        ("petroleo_gas_sub", "Petróleo e Gás (Subsequente)"),
        ("redes_comp_sub", "Redes de Computadores (Subsequente)"),
        ("manutencao_suporte_sub", "Manutenção e Suporte em Informática (Subsequente)"),
        ("informatica_sub", "Informática (Subsequente)"),
        ("seguranca_trabalho_sub", "Segurança do Trabalho (Subsequente)"),
        ("estradas_sub", "Estradas (Subsequente)"),

        # Cursos FIC
        ("implanta_voip_fic", "Implantação de Serviços VoIP (FIC)"),
        ("aplicador_ceramico_fic", "Aplicador de Revestimento Cerâmico (FIC)"),
        ("artesanato_reciclavel_fic", "Artesanato com Material Reciclável (FIC)"),

        # Graduação – Engenharias
        ("engenharia_civil", "Engenharia Civil"),
        ("engenharia_energia", "Engenharia de Energia"),
        ("engenharia_sanitaria", "Engenharia Sanitária e Ambiental"),

        # Graduação – Tecnologias (Tec. Superiores)
        ("tecnologia_ads", "Tecnologia em Análise e Desenvolvimento de Sistemas"),
        ("tecnologia_com_exterior", "Tecnologia em Comércio Exterior"),
        ("tecnologia_gestao_publica", "Tecnologia em Gestão Pública"),
        ("tecnologia_redes_comp", "Tecnologia em Redes de Computadores"),

        # Pós‑Graduação – Especializações
        ("esp_seguranca_trab", "Especialização em Engenharia de Segurança do Trabalho"),
        ("esp_ensino_geociencias", "Especialização em Ensino de Geociências"),
        ("esp_gestao_ambiental", "Especialização em Gestão Ambiental"),

        # Pós‑Graduação – Mestrados
        ("mestrado_prof_ensino_fis", "Mestrado Profissional em Ensino de Física"),
        ("mestrado_prof_recursos_nat", "Mestrado Profissional em Uso Sustentável de Recursos Naturais"),

        # Pós‑Graduação – Doutorado
        ("doutorado_educacao_prof", "Doutorado Acadêmico em Educação Profissional"),
    ]

    for codigo, nome in cursos_data:
        Cursos.objects.get_or_create(nome=nome)


def reverse_populate_cursos(apps, schema_editor):
    Cursos = apps.get_model('api', 'Cursos')
    Cursos.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_cursos_alter_auxilio_descricao_alter_auxilio_nome_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cursos',
            name='nome',
            field=models.CharField(choices=[('administracao', 'Administração'), ('controle_ambiental', 'Controle Ambiental'), ('edificacoes', 'Edificações'), ('eletrotecnica', 'Eletrotécnica'), ('geologia', 'Geologia'), ('informatica_internet', 'Informática para Internet'), ('manutencao_suporte', 'Manutenção e Suporte em Informática'), ('mecanica', 'Mecânica'), ('mineracao', 'Mineração'), ('controle_ambiental_sub', 'Controle Ambiental (Subsequente)'), ('edificacoes_sub', 'Edificações (Subsequente)'), ('eletrotecnica_sub', 'Eletrotécnica (Subsequente)'), ('geologia_sub', 'Geologia (Subsequente)'), ('mecanica_sub', 'Mecânica (Subsequente)'), ('mineracao_sub', 'Mineração (Subsequente)'), ('petroleo_gas_sub', 'Petróleo e Gás (Subsequente)'), ('redes_comp_sub', 'Redes de Computadores (Subsequente)'), ('manutencao_suporte_sub', 'Manutenção e Suporte em Informática (Subsequente)'), ('informatica_sub', 'Informática (Subsequente)'), ('seguranca_trabalho_sub', 'Segurança do Trabalho (Subsequente)'), ('estradas_sub', 'Estradas (Subsequente)'), ('implanta_voip_fic', 'Implantação de Serviços VoIP (FIC)'), ('aplicador_ceramico_fic', 'Aplicador de Revestimento Cerâmico (FIC)'), ('artesanato_reciclavel_fic', 'Artesanato com Material Reciclável (FIC)'), ('engenharia_civil', 'Engenharia Civil'), ('engenharia_energia', 'Engenharia de Energia'), ('engenharia_sanitaria', 'Engenharia Sanitária e Ambiental'), ('tecnologia_ads', 'Tecnologia em Análise e Desenvolvimento de Sistemas'), ('tecnologia_com_exterior', 'Tecnologia em Comércio Exterior'), ('tecnologia_gestao_publica', 'Tecnologia em Gestão Pública'), ('tecnologia_redes_comp', 'Tecnologia em Redes de Computadores'), ('esp_seguranca_trab', 'Especialização em Engenharia de Segurança do Trabalho'), ('esp_ensino_geociencias', 'Especialização em Ensino de Geociências'), ('esp_gestao_ambiental', 'Especialização em Gestão Ambiental'), ('mestrado_prof_ensino_fis', 'Mestrado Profissional em Ensino de Física'), ('mestrado_prof_recursos_nat', 'Mestrado Profissional em Uso Sustentável de Recursos Naturais'), ('doutorado_educacao_prof', 'Doutorado Acadêmico em Educação Profissional')], default='', max_length=100),
        ),
        migrations.RunPython(populate_cursos, reverse_populate_cursos),
    ]
