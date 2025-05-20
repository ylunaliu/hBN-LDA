#!/usr/bin/env python
# Pseudobands!
import sys
import h5py
import numpy as np
try:
    from progress.bar import Bar
except:
    Bar = None
if len(sys.argv)!=5:
    print ('Usage: input_wfn.h5 output_wfn.h5 E0 p')
    print ('E0: protection window, in Ry (ex: 4)')
    print ('p: pseudizing energy window in units of avg. band energy (ex: 0.02)')
    sys.exit()
fname_in, fname_out = sys.argv[1:3]
emin, percent_window = map(float, sys.argv[3:5])
f_in = h5py.File(fname_in)
f_out = h5py.File(fname_out, 'w')
print('Input file: {}'.format(fname_in))
print('Output file: {}'.format(fname_out))
print('Protection window: {} Ry'.format(emin))
print('Superband width: {} %'.format(percent_window*100))
print('')
en_orig = f_in['mf_header/kpoints/el'][()]
nb_orig = f_in['mf_header/kpoints/mnband'][()]
print('Original number of bands: {}'.format(nb_orig))
# Ok, so e_min and e_max doesn`t really work, we just take the average
en_min = np.mean(en_orig[0,:,:], axis=0)
en_max = np.mean(en_orig[0,:,:], axis=0)
ind = np.arange(nb_orig)
#print(en_max)
#print(ind[en_min > emin])
nb_fixed = ind[en_min > emin][0]
#print(en_max)
print('Number of bands in the protection window: {}'.format(nb_fixed))
blocks = []
nb_out = nb_fixed
first_idx = nb_fixed
#print(first_en,delta_en,last_en)
while True:
    first_en = en_min[first_idx]
    delta_en = first_en * percent_window
    last_en = first_en + delta_en
    try:
        last_idx = ind[en_max > last_en][0]
        print(last_idx)
        blocks.append((first_idx, last_idx-1))
        print(blocks,len(blocks))
        nb_out += 1
        first_idx = last_idx
    except:
        last_idx = nb_orig-1
        blocks.append((first_idx, last_idx-1))
        nb_out += 1
        break
print('Number of bands in the output file: {}'.format(nb_out))
f_out.copy(f_in['mf_header'], 'mf_header')
f_out.create_group('wfns')
f_out.copy(f_in['wfns/gvecs'], 'wfns/gvecs')
f_out['mf_header/kpoints/mnband'][()] = nb_out
def resize(name):
    f_out.move(name, name+'_orig')
    shape = list(f_out[name+'_orig'].shape)
    shape[-1] = nb_out
    f_out.create_dataset(name, shape, dtype='d')
    f_out[name][:,:,:nb_out] = f_out[name+'_orig'][:,:,:nb_out]
    del f_out[name+'_orig']
resize('mf_header/kpoints/occ')
resize('mf_header/kpoints/el')
print('Copying protected bands')
shape = list(f_in['wfns/coeffs'].shape)
print (shape)
shape[0] = nb_out
print (shape)
print (nb_out)
print (nb_fixed)
f_out.create_dataset('wfns/coeffs', shape, 'd')
f_out['wfns/coeffs'][:nb_fixed,:,:] = f_in['wfns/coeffs'][:nb_fixed,:,:]
print('Creating {} superbands'.format(len(blocks)))
ib = nb_fixed
print(ib)
if Bar is not None:
    bar = Bar('Creating superbands', max=nb_orig-nb_fixed, bar_prefix=' [', bar_suffix='] ',
        fill='#', suffix='%(percent)d%% - Remaining: %(eta_td)s')
for b in blocks:
    if Bar is not None:
        bar.next(b[1]-b[0]+1)
    f_out['wfns/coeffs'][ib,:,:] = f_in['wfns/coeffs'][b[0]:b[1]+1,:,:].sum(axis=0)
    f_out['mf_header/kpoints/el'][:,:,ib] = f_in['mf_header/kpoints/el'][:,:,b[0]:b[1]+1].mean(axis=-1)
    ib += 1
if Bar is not None:
    bar.finish()
print('')
print('All done!')
f_out.close()
f_in.close()