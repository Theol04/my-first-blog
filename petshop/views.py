from django.shortcuts import render, get_object_or_404, redirect
from .models import Animal
from .models import Equipement
from .forms import MoveForm
# Create your views here.

def animal_list(request):
    animals = Animal.objects.filter()
    equipements = Equipement.objects.filter()
    return render(request, 'petshop/animal_list.html', {'animals':animals, 'equipements':equipements})

def equipement_detail(request, id_equip):
    equipements = get_object_or_404(Equipement, id_equip=id_equip)
    animals = Animal.objects.filter()
    return render(request, 'petshop/equipement_detail.html', {'animals':animals, 'equipements':equipements})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)

    if request.method == "POST":
        form=MoveForm(request.POST, instance=animal)

        if form.is_valid():
            if form.data['lieu'] == "litiere":
                form.save(commit=False)
                if animal.etat == 'endormi':
                    ancien_lieu.disponibilite = "Libre"
                    animal.etat = 'affame'
                    animal.save()
                    ancien_lieu.save()
                    return redirect('animal_detail', id_animal=id_animal)
                else:
                    return render(request, "petshop/animal_detail.html", {'message': f"Désolé {id_animal} ne dors pas."})

            if form.data['lieu'] == "roue":
                form.save(commit=False)

                if animal.etat == 'repus':
                    if animal.lieu.disponibilite == 'Libre':
                        
                        ancien_lieu.disponibilite = 'Libre'
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                        nouveau_lieu.disponibilite = "Occupe"
                        animal.etat = 'fatigue'
                        ancien_lieu.save()
                        nouveau_lieu.save()
                        animal.save()
                        return redirect('animal_detail', id_animal=id_animal)
                    else:
                        return render(request, "petshop/animal_detail.html", {'message': f"Désolé la roue est occupée ."})
                else :
                    return render(request, "petshop/animal_detail.html", {'message': f"Désolé {id_animal} n'est pas repus."})
            
            
            if form.data['lieu'] == "mangeoire":
                form.save(commit=False)
                if  animal.etat == 'affame':
                    if animal.lieu.disponibilite == 'Libre':

                        ancien_lieu.disponibilite = 'Libre'
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                        nouveau_lieu.disponibilite = "Occupe"
                        animal.etat = 'repus'
                        nouveau_lieu.save()
                        ancien_lieu.save()
                        animal.save()

                        return redirect('animal_detail', id_animal=id_animal)
                    else:
                        return render(request, "petshop/animal_detail.html", {'message': f"Désolé la mangeoire est occupée."})

                else :
                    return render(request, "petshop/animal_detail.html", {'message': f"Désolé {id_animal} n'a pas faim."})

            

            if form.data['lieu'] == "nid":
                form.save(commit=False)
                if animal.etat == 'fatigue':
                    if animal.lieu.disponibilite == 'Libre':

                        ancien_lieu.disponibilite = "Libre"
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                        nouveau_lieu.disponibilite = "Occupe"
                        animal.etat = 'endormi'
                        nouveau_lieu.save()
                        ancien_lieu.save()
                        animal.save()

                        return redirect('animal_detail', id_animal=id_animal)
                    else:
                        return render(request, "petshop/animal_detail.html", {'message': f"Désolé le nid est occupé."})
                else :
                    return render(request, "petshop/animal_detail.html", {'message': f"Désolé {id_animal} n'a pas envie de dormir."})

        else:
            form = MoveForm()
            return render(request,
                    'petshop/animal_detail.html',
                    {'animal': animal, 'lieu': animal.lieu, 'form': form})
    else:
        form = MoveForm()
        return render(request,
                'petshop/animal_detail.html',
                {'animal': animal, 'lieu': animal.lieu, 'form': form})
